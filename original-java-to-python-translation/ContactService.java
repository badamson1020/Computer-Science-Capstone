package edu.snhu.badamson.contact;

import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import lombok.EqualsAndHashCode;

public class ContactService {
	
	private List<Contact> contacts;
		
	public ContactService() {
		contacts = new ArrayList<>();			
	}

	/**
	 * Adds a new contact to the service
	 * Checks that the ID is unique
	 * @param newContact is the contact to add
	 * @throws IllegalArgumentException if the contact is null or a duplicate ID.
	 */
	public void add(Contact newContact) {
		 if (newContact == null) {
	            throw new IllegalArgumentException("Contact cannot be null.");
		 }
		
		boolean isDuplicate = false;
		for (Contact contact: contacts) {
			if (contact.getId().equals(newContact.getId())) {
				isDuplicate = true;
				break;
			}
		}
		
		if (isDuplicate) {
			throw new IllegalArgumentException("Cannot add school with duplicate ID: " + newContact.getId());
		}
		contacts.add(newContact);		
	}
	
	/**
	 * Deletes a contact by its ID.
	 * @param id The ID of the contact to be deleted.
	 * @throws IllegalArgumentException if the ID is null.
	 * @throws NoSuchElementException if no contact with the given ID exists.
	 */
	public void delete(String id) {
	    if (id == null) {
	        throw new IllegalArgumentException("ID cannot be null.");
	    }
	    
	    Contact contactToDelete = null;
	    
	    for (Contact contact : contacts) {
	        if (contact.getId().equals(id)) {
	            contactToDelete = contact;
	            break;
	        }
	    }
	    
	    if (contactToDelete == null) {
	        throw new NoSuchElementException("Contact with ID " + id + " does not exist.");
	    }
	    
	    contacts.remove(contactToDelete);
	}
	
	/**
	 * Updates an existing contact, ID cannot be updated. 
	 * @param updatedContact The contact with updated fields.
     * @throws IllegalArgumentException if the contact or its ID is null.
     * @throws NoSuchElementException if no contact with the ID exists.
	 */
	public void edit(Contact updatedContact) {
		if (updatedContact == null || updatedContact.getId() == null) {
	        throw new IllegalArgumentException("The contact and/or its ID cannot be null.");
	    }
	    
	    Contact existingContact = get(updatedContact.getId());
	    
	    if (existingContact == null) {
	        throw new NoSuchElementException("Contact with ID " + updatedContact.getId() + " does not exist.");
	    }
	    
	    existingContact.setFirstName(updatedContact.getFirstName());
	    existingContact.setLastName(updatedContact.getLastName());
	    existingContact.setNumber(updatedContact.getNumber());
	    existingContact.setAddress(updatedContact.getAddress());
	}
	
	/**
	 * Get the contact by id.
	 * Returns the contact if found, otherwise returns null.
	 * @param id - the contact id
	 * @return the contact or null if id does not exist.
	 * @throws IllegalArgumentException if the ID is null.
	 */
	public Contact get(String id) {
		if (id == null) {
	        throw new IllegalArgumentException("ID cannot be null.");
	    }
		
		Contact foundContact = null;
		
		for (Contact contact: contacts) {
			if(contact.getId().equals(id)) {
				foundContact = contact;
				break;
			}
		}
		return foundContact;
	}
	
	/**
	 * Gets a copy of the list of contacts, preventing changes to the internal contact list.
	 * Returns an empty list if none exists.
	 * @return - the list of schools or none if it is empty.
	 */
	public List<Contact> getAll() {
	    List<Contact> contactCopy = new ArrayList<>(contacts);
	    
	    return contactCopy;
	}
}
