package edu.snhu.badamson.contact;

import java.util.List;
import java.util.NoSuchElementException;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public class ContactServiceTest {

	private ContactService service;
	
	@BeforeEach
	public void setup() {
		service = new ContactService();		
	}	
	
	/////////////////////////////////////////////////////////////
	/// Test Add
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testAdd_withNewElement_successfullyAdds() {
		Contact newContact = new Contact("12", "Beth", "Adams", "1234567890", "Colorado");
		
		service.add(newContact);
		
		Assertions.assertEquals(service.get(newContact.getId()), newContact);
	}
	
	@Test
	public void testAdd_withDuplicateElement_throwsIllegalArgumentException() {
		Contact newContact = new Contact("12", "Beth", "Adams", "1234567890", "Colorado");
		
		service.add(newContact);
		
		Assertions.assertNotNull(service.get(newContact.getId()));	
		
		Assertions.assertThrows(IllegalArgumentException.class, () -> service.add(newContact));

	}
	
	@Test
	public void testAdd_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> service.add(null));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test Delete
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testDelete_withExistingElement_successfullyDeletes() {
		Contact newContact = new Contact("12", "Beth", "Adams", "1234567890", "Colorado");
		
		service.add(newContact);
		
		Assertions.assertNotNull(service.get(newContact.getId())); 
	    
	    service.delete(newContact.getId()); 
	    
	    Assertions.assertNull(service.get(newContact.getId())); 
	}
	
	@Test 
	public void testDelete_withNonExistentId_throwsNoSuchElementException() {
		String nonExistentId = "123";
		
		Assertions.assertNull(service.get(nonExistentId));
		
		Assertions.assertThrows(NoSuchElementException.class, () -> service.delete(nonExistentId));
	}
	
	@Test
	public void testDelete_withNullId_throwsIllegalArgumentException() {
	    Assertions.assertThrows(IllegalArgumentException.class, () -> service.delete(null));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test Edit
	/////////////////////////////////////////////////////////////

	// Keeps the ID the same, but changes the other fields.
	@Test
	public void testEdit_withUpdatedContact_updatesFieldsSuccessfully() {
	    Contact newContact = new Contact("1", "Beth", "Adams", "0123456789", "Colorado");
	    service.add(newContact);

	    Contact updatedContact = new Contact("1", "Josh", "Smith", "0987654321", "New Jersey");
	    service.edit(updatedContact);

	    Contact checkedContact = service.get("1");

	    Assertions.assertEquals("Josh", checkedContact.getFirstName());
	    Assertions.assertEquals("Smith", checkedContact.getLastName());
	    Assertions.assertEquals("0987654321", checkedContact.getNumber());
	    Assertions.assertEquals("New Jersey", checkedContact.getAddress());
	}
	
	@Test
	public void testEdit_withNonExistingContact_throwsNoSuchElementException() {
	    // A new contact is created, but never added to the ContactService.
	    Contact newContact = new Contact("123", "Non", "Existent", "0987654321", "Nowhere");

	    Assertions.assertThrows(NoSuchElementException.class, () -> service.edit(newContact));
	}
		
	@Test
	public void testEdit_withNullValue_throwsIllegalArgumentException() {
	    Assertions.assertThrows(IllegalArgumentException.class, () -> service.edit(null));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test Get
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testGet_withValidId_returnsCorrectContact() {
	    Contact newContact = new Contact("12", "Beth", "Adams", "1234567890", "Colorado");
	    service.add(newContact);

	    Contact selectedContact = service.get(newContact.getId());
	        
	    Assertions.assertNotNull(selectedContact);
	    Assertions.assertEquals(newContact, selectedContact); 
	}

	@Test
	public void testGet_withInvalidId_returnsNull() {		
		Contact newContact = new Contact("12", "Beth", "Adams", "1234567890", "Colorado");
	    service.add(newContact);
		
		Contact selectedContact = service.get("234");
	        
	    Assertions.assertNull(selectedContact);
	}

	@Test
	public void testGet_withNullId_throwsIllegalArgumentException() {
	    Assertions.assertThrows(IllegalArgumentException.class, () -> service.get(null));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test GetAll
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testGetAll_withMultipleContacts_returnsAllContacts() {
	    Contact contact1 = new Contact("1", "Beth", "Adams", "1234567890", "Colorado");
	    Contact contact2 = new Contact("2", "Josh", "Smith", "0987654321", "California");
	    service.add(contact1);
	    service.add(contact2);
	    
	    List<Contact> allContacts = service.getAll();
	    
	    Assertions.assertEquals(2, allContacts.size());
	    Assertions.assertTrue(allContacts.contains(contact1));
	    Assertions.assertTrue(allContacts.contains(contact2));
	}
	
	@Test
	public void testGetAll_withNoContacts_returnsEmptyList() {
	    List<Contact> allContacts = service.getAll();
	    
	    Assertions.assertTrue(allContacts.isEmpty());
	}
	
	@Test
	public void testGetAll_afterDeletingContact_returnsRemainingContacts() {
	    Contact contact1 = new Contact("1", "Beth", "Adams", "1234567890", "Colorado");
	    Contact contact2 = new Contact("2", "Josh", "Smith", "0987654321", "California");
	    service.add(contact1);
	    service.add(contact2);
	    
	    service.delete(contact1.getId());
	    
	    List<Contact> allContacts = service.getAll();
	    
	    Assertions.assertEquals(1, allContacts.size());
	    Assertions.assertTrue(allContacts.contains(contact2));
	    Assertions.assertFalse(allContacts.contains(contact1));
	}	
}
