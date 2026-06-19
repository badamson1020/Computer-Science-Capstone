package edu.snhu.badamson.task;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import lombok.EqualsAndHashCode;

public class TaskTest {
	// All VALID variables are also representative of the minimum allowed length for those fields.
	final String VALID_ID = "1";
	final String VALID_NAME = "A";
	final String VALID_DESCRIPTION = "B";
	final String TEN_LENGTH_INPUT = "123456789A";
	final String TWENTY_LENGTH_INPUT = "12345678901234567890";
	final String FIFTY_LENGTH_INPUT = "12345678901234567890123456789012345678901234567890";
	
	/////////////////////////////////////////////////////////////
	/// Test id
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testId_withMinLength_isValid() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
		
		Assertions.assertEquals(VALID_ID, testTask.getId());		
	}
	
	@Test
	public void testId_withMaxLength_isValid() {
		Task testTask = new Task(TEN_LENGTH_INPUT, VALID_NAME, VALID_DESCRIPTION);
		
		Assertions.assertEquals(TEN_LENGTH_INPUT, testTask.getId());	
	}
	
	@Test
	public void testId_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Task(null, VALID_NAME, VALID_DESCRIPTION));
	}		
	
	@Test
	public void testId_withMoreThanMaxLength_throwsIllegalArgumentException() {	
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Task(TEN_LENGTH_INPUT + "A", VALID_NAME, VALID_DESCRIPTION));
	}
	
	@Test
	public void testId_withEmptyValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Task("", VALID_NAME, VALID_DESCRIPTION));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test name
	/////////////////////////////////////////////////////////////
	
	// Each test type is run once for the task constructor and once for the public setter method.
	@Test
	public void testName_withMinLength_isValid() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
		
		Assertions.assertEquals(VALID_NAME, testTask.getName());		
	}
	
	@Test
	public void testSetName_withMinLength_isValid() {
		Task testTask = new Task(VALID_ID, TEN_LENGTH_INPUT, VALID_DESCRIPTION);
		testTask.setName(VALID_NAME);
		
		Assertions.assertEquals(VALID_NAME, testTask.getName());
	}
	
	@Test
	public void testName_withMaxLength_isValid() {
		Task testTask = new Task(VALID_ID, TWENTY_LENGTH_INPUT, VALID_DESCRIPTION);
		
		Assertions.assertEquals(TWENTY_LENGTH_INPUT, testTask.getName());	
	}
	
	@Test
	public void testSetName_withMaxLength_isValid() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
		testTask.setName(TWENTY_LENGTH_INPUT);
		
		Assertions.assertEquals(TWENTY_LENGTH_INPUT, testTask.getName());
	}
	
	@Test
	public void testName_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Task(VALID_ID, null, VALID_DESCRIPTION));
	}	
	
	@Test
	public void testSetName_withNullValue_throwsIllegalArgumentException() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testTask.setName(null));
	}
	
	@Test
	public void testName_withMoreThanMaxLength_throwsIllegalArgumentException() {	
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Task(VALID_ID, TWENTY_LENGTH_INPUT + "A", VALID_DESCRIPTION));
	}
	
	@Test
	public void testSetName_withMoreThanMaxLength_throwsIllegalArgumentException() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testTask.setName(TWENTY_LENGTH_INPUT + "A"));
	}
	
	@Test
	public void testName_withEmptyValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Task(VALID_ID, "", VALID_DESCRIPTION));
	}
	
	@Test
	public void testSetName_withEmptyValue_throwsIllegalArgumentException() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testTask.setName(""));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test description
	/////////////////////////////////////////////////////////////
	
	// Each test type is run once for the task constructor and once for the public setter method.
	@Test
	public void testDescription_withMinLength_isValid() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
		
		Assertions.assertEquals(VALID_DESCRIPTION, testTask.getDescription());		
	}
	
	@Test
	public void testSetDescription_withMinLength_isValid() {
		Task testTask = new Task(VALID_ID, VALID_NAME, TEN_LENGTH_INPUT);
		testTask.setDescription(VALID_DESCRIPTION);
		
		Assertions.assertEquals(VALID_DESCRIPTION, testTask.getDescription());
	}
	
	@Test
	public void testDescription_withMaxLength_isValid() {
		Task testTask = new Task(VALID_ID, VALID_NAME, FIFTY_LENGTH_INPUT);
		
		Assertions.assertEquals(FIFTY_LENGTH_INPUT, testTask.getDescription());	
	}
	
	@Test
	public void testSetDescription_withMaxLength_isValid() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
		testTask.setDescription(FIFTY_LENGTH_INPUT);
		
		Assertions.assertEquals(FIFTY_LENGTH_INPUT, testTask.getDescription());
	}
	
	@Test
	public void testDescription_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Task(VALID_ID, VALID_NAME, null));
	}	
	
	@Test
	public void testSetDescription_withNullValue_throwsIllegalArgumentException() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testTask.setDescription(null));
	}
	
	@Test
	public void testDescription_withMoreThanMaxLength_throwsIllegalArgumentException() {	
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Task(VALID_ID, VALID_NAME, FIFTY_LENGTH_INPUT + "A"));
	}
	
	@Test
	public void testSetDescription_withMoreThanMaxLength_throwsIllegalArgumentException() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testTask.setDescription(FIFTY_LENGTH_INPUT + "A"));
	}
	
	@Test
	public void testDescription_withEmptyValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Task(VALID_ID, VALID_NAME, ""));
	}
	
	@Test
	public void testSetDescription_withEmptyValue_throwsIllegalArgumentException() {
		Task testTask = new Task(VALID_ID, VALID_NAME, VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testTask.setDescription(""));
	}
}
