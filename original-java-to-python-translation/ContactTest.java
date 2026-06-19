package edu.snhu.badamson.contact;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public class ContactTest {
	
	// All VALID variables are also representative of the minimum allowed length for those fields.
	final String VALID_ID = "1";
	final String VALID_FIRST_NAME = "A";
	final String VALID_LAST_NAME = "B";
	final String VALID_NUMBER = "1234567890";
	final String VALID_ADDRESS = "C";
	final String TEN_LENGTH_INPUT = "123456789A";
	final String THIRTY_LENGTH_INPUT = "123456789012345678901234567890";
	final String SHORT_INPUT = "2A";
	
	/////////////////////////////////////////////////////////////
	/// Test id
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testId_withMinLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		
		Assertions.assertEquals(VALID_ID, testContact.getId());		
	}
	
	@Test
	public void testId_withMaxLength_isValid() {
		Contact testContact = new Contact(TEN_LENGTH_INPUT, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		
		Assertions.assertEquals(TEN_LENGTH_INPUT, testContact.getId());	
	}
	
	@Test
	public void testId_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(null, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS));
	}		
	
	@Test
	public void testId_withMoreThanMaxLength_throwsIllegalArgumentException() {	
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(TEN_LENGTH_INPUT + "A", VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS));
	}
	
	@Test
	public void testId_withEmptyValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact("", VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test firstName
	/////////////////////////////////////////////////////////////
	
	// Each test type is run once for the contact constructor and once for the public setter method.
	@Test
	public void testFirstName_withMinLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		
		Assertions.assertEquals(VALID_FIRST_NAME, testContact.getFirstName());		
	}
	
	@Test
	public void testSetFirstName_withMinLength_isValid() {
		Contact testContact = new Contact(VALID_ID, TEN_LENGTH_INPUT, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		testContact.setFirstName(VALID_FIRST_NAME);
		
		Assertions.assertEquals(VALID_FIRST_NAME, testContact.getFirstName());
	}
	
	@Test
	public void testFirstName_withMaxLength_isValid() {
		Contact testContact = new Contact(VALID_ID, TEN_LENGTH_INPUT, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		
		Assertions.assertEquals(TEN_LENGTH_INPUT, testContact.getFirstName());	
	}
	
	@Test
	public void testSetFirstName_withMaxLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		testContact.setFirstName(TEN_LENGTH_INPUT);
		
		Assertions.assertEquals(TEN_LENGTH_INPUT, testContact.getFirstName());
	}
	
	@Test
	public void testFirstName_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, null, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS));
	}	
	
	@Test
	public void testSetFirstName_withNullValue_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setFirstName(null));
	}
	
	@Test
	public void testFirstName_withMoreThanMaxLength_throwsIllegalArgumentException() {	
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, TEN_LENGTH_INPUT + "A", VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS));
	}
	
	@Test
	public void testSetFirstName_withMoreThanMaxLength_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setFirstName(TEN_LENGTH_INPUT + "A"));
	}
	
	@Test
	public void testFirstName_withEmptyValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, "", VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS));
	}
	
	@Test
	public void testSetFirstName_withEmptyValue_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setFirstName(""));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test lastName
	/////////////////////////////////////////////////////////////
	
	// Each test type is run once for the contact constructor and once for the public setter method.
	@Test
	public void testLastName_withMinLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		
		Assertions.assertEquals(VALID_LAST_NAME, testContact.getLastName());		
	}
	
	@Test
	public void testSetLastName_withMinLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, TEN_LENGTH_INPUT, VALID_NUMBER, VALID_ADDRESS);
		testContact.setLastName(VALID_LAST_NAME);
		
		Assertions.assertEquals(VALID_LAST_NAME, testContact.getLastName());
	}
	
	@Test
	public void testLastName_withMaxLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, TEN_LENGTH_INPUT, VALID_NUMBER, VALID_ADDRESS);
		
		Assertions.assertEquals(TEN_LENGTH_INPUT, testContact.getLastName());	
	}
	
	@Test
	public void testSetLastName_withMaxLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		testContact.setLastName(TEN_LENGTH_INPUT);
		
		Assertions.assertEquals(TEN_LENGTH_INPUT, testContact.getLastName());
	}
	
	@Test
	public void testLastName_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, VALID_FIRST_NAME, null, VALID_NUMBER, VALID_ADDRESS));
	}	
	
	@Test
	public void testSetLastName_withNullValue_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setLastName(null));
	}
	
	@Test
	public void testLastName_withMoreThanMaxLength_throwsIllegalArgumentException() {	
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, VALID_FIRST_NAME, TEN_LENGTH_INPUT + "A", VALID_NUMBER, VALID_ADDRESS));
	}
	
	@Test
	public void testSetLastName_withMoreThanMaxLength_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setLastName(TEN_LENGTH_INPUT + "A"));
	}
	
	@Test
	public void testLastName_withEmptyValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, VALID_FIRST_NAME, "", VALID_NUMBER, VALID_ADDRESS));
	}
	
	@Test
	public void testSetLastName_withEmptyValue_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setLastName(""));
	}	
	
	/////////////////////////////////////////////////////////////
	/// Test number
	/////////////////////////////////////////////////////////////
	
	// Each test type is run once for the contact constructor and once for the public setter method.
	@Test
	public void testNumber_withTenCharacters_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		
		Assertions.assertEquals(VALID_NUMBER, testContact.getNumber());	
	}
	
	@Test
	public void testSetNumber_withTenCharacters_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, TEN_LENGTH_INPUT, VALID_ADDRESS);
		testContact.setNumber(VALID_NUMBER);
		
		Assertions.assertEquals(VALID_NUMBER, testContact.getNumber());
	}
	
	@Test
	public void testNumber_withLessThanTenCharacters_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, SHORT_INPUT, VALID_ADDRESS));
	}	
	
	@Test
	public void testSetNumber_withLessThanTenCharacters_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setNumber(SHORT_INPUT));
	}
	
	@Test
	public void testNumber_withMoreThanTenCharacters_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, THIRTY_LENGTH_INPUT, VALID_ADDRESS));
	}	
	
	@Test
	public void testSetNumber_withMoreThanTenCharacters_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setNumber(THIRTY_LENGTH_INPUT));
	}
	
	@Test
	public void testNumber_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, null, VALID_ADDRESS));
	}	
	
	@Test
	public void testSetNumber_withNullValue_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setNumber(null));
	}	
		
	/////////////////////////////////////////////////////////////
	/// Test address
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testAddress_withMinLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		
		Assertions.assertEquals(VALID_ADDRESS, testContact.getAddress());		
	}
	
	@Test
	public void testSetAddress_withMinLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, TEN_LENGTH_INPUT);
		testContact.setAddress(VALID_ADDRESS);
		
		Assertions.assertEquals(VALID_ADDRESS, testContact.getAddress());
	}
	
	@Test
	public void testAddress_withMaxLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, THIRTY_LENGTH_INPUT);
		
		Assertions.assertEquals(THIRTY_LENGTH_INPUT, testContact.getAddress());	
	}
	
	@Test
	public void testSetAddress_withMaxLength_isValid() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
		testContact.setAddress(THIRTY_LENGTH_INPUT);
		
		Assertions.assertEquals(THIRTY_LENGTH_INPUT, testContact.getAddress());
	}
	
	@Test
	public void testAddress_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, null));
	}	
	
	@Test
	public void testSetAddress_withNullValue_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setAddress(null));
	}
	
	@Test
	public void testAddress_withMoreThanMaxLength_throwsIllegalArgumentException() {	
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, THIRTY_LENGTH_INPUT + "A"));
	}
	
	@Test
	public void testSetAddress_withMoreThanMaxLength_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setAddress(THIRTY_LENGTH_INPUT + "A"));
	}
	
	@Test
	public void testAddress_withEmptyValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, ""));
	}
	
	@Test
	public void testSetAddress_withEmptyValue_throwsIllegalArgumentException() {
		Contact testContact = new Contact(VALID_ID, VALID_FIRST_NAME, VALID_LAST_NAME, VALID_NUMBER, VALID_ADDRESS);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testContact.setAddress(""));
	}	
}
