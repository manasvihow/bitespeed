from datetime import datetime
from fastapi import APIRouter
from sqlmodel import Session, select

from ..database import engine
from ..models import Contact
from ..schemas import IdentifyRequest, IdentifyResponse, ContactResponse

router = APIRouter()

@router.post("/identify", response_model=IdentifyResponse)
def identify(request: IdentifyRequest):
    with Session(engine) as session:
        # Step 1: Find all contacts that directly match the request
        direct_matches = session.exec(
            select(Contact).where(
                (Contact.email == request.email and request.email is not None) |
                (Contact.phoneNumber == request.phoneNumber and request.phoneNumber is not None)
            )
        ).all()

        if not direct_matches:
            # This is a brand new contact, create a primary record
            new_contact = Contact(email=request.email, phoneNumber=request.phoneNumber, linkPrecedence="primary")
            session.add(new_contact)
            session.commit()
            session.refresh(new_contact)
            return IdentifyResponse(
                contact=ContactResponse(
                    primaryContactId=new_contact.id,
                    emails=[new_contact.email] if new_contact.email else [],
                    phoneNumbers=[new_contact.phoneNumber] if new_contact.phoneNumber else [],
                    secondaryContactIds=[],
                )
            )

        # Step 2: Find all contacts that are part of the same identity groups
        contact_ids_to_fetch = set()
        for c in direct_matches:
            if c.linkedId:
                contact_ids_to_fetch.add(c.linkedId)
            else:
                contact_ids_to_fetch.add(c.id)
        
        all_involved_contacts = session.exec(
            select(Contact).where(
                (Contact.id.in_(contact_ids_to_fetch)) |
                (Contact.linkedId.in_(contact_ids_to_fetch))
            )
        ).all()

        # Step 3: Determine the ultimate primary contact (the oldest one)
        ultimate_primary_contact = sorted(all_involved_contacts, key=lambda c: c.createdAt)[0]

        # Step 4: Update all other contacts to link to the ultimate primary
        for contact in all_involved_contacts:
            if contact.id != ultimate_primary_contact.id:
                if contact.linkPrecedence != "secondary" or contact.linkedId != ultimate_primary_contact.id:
                    contact.linkPrecedence = "secondary"
                    contact.linkedId = ultimate_primary_contact.id
                    contact.updatedAt = datetime.utcnow()
                    session.add(contact)
        
        # Step 5: Check if the request contains new info not present in the entire group
        all_emails = {c.email for c in all_involved_contacts if c.email}
        all_phones = {c.phoneNumber for c in all_involved_contacts if c.phoneNumber}

        if (request.email and request.email not in all_emails) or \
           (request.phoneNumber and request.phoneNumber not in all_phones):
            new_secondary_contact = Contact(
                email=request.email,
                phoneNumber=request.phoneNumber,
                linkedId=ultimate_primary_contact.id,
                linkPrecedence="secondary",
            )
            session.add(new_secondary_contact)
            all_involved_contacts.append(new_secondary_contact)
        
        session.commit()

        # Step 6: Prepare the final consolidated response
        final_emails = sorted(list(set(c.email for c in all_involved_contacts if c.email)))
        final_phones = sorted(list(set(c.phoneNumber for c in all_involved_contacts if c.phoneNumber)))
        
        primary_email = ultimate_primary_contact.email
        primary_phone = ultimate_primary_contact.phoneNumber
        
        if primary_email in final_emails:
            final_emails.insert(0, final_emails.pop(final_emails.index(primary_email)))
        if primary_phone in final_phones:
            final_phones.insert(0, final_phones.pop(final_phones.index(primary_phone)))

        secondary_ids = [c.id for c in all_involved_contacts if c.linkPrecedence == 'secondary']

        return IdentifyResponse(
            contact=ContactResponse(
                primaryContactId=ultimate_primary_contact.id,
                emails=list(dict.fromkeys(final_emails)),
                phoneNumbers=list(dict.fromkeys(final_phones)),
                secondaryContactIds=sorted(list(set(secondary_ids))),
            )
        )