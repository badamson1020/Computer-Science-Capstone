package edu.snhu.badamson.appointment;

import java.util.Calendar;
import java.util.Date;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public class AppointmentTest {
	// All VALID variables are also representative of the minimum allowed length for those fields.
	private final String VALID_ID = "1";
	private final String VALID_DESCRIPTION = "B";
	private final String TEN_LENGTH_INPUT = "123456789A";
	private final String FIFTY_LENGTH_INPUT = "12345678901234567890123456789012345678901234567890";
	
	 // Method used to create new future dates for testing.
    private Date getTodayPlusDays(int days) {
        Calendar cal = Calendar.getInstance();
        cal.add(Calendar.DATE, days);
        return cal.getTime();
    }

    private Date getPastDate() {
        Calendar cal = Calendar.getInstance();
        cal.set(2021, Calendar.DECEMBER, 22); 
        return cal.getTime();
    }
	
	/////////////////////////////////////////////////////////////
	/// Test id
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testId_withMinLength_isValid() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
		
		Assertions.assertEquals(VALID_ID, testAppointment.getId());		
	}
	
	@Test
	public void testId_withMaxLength_isValid() {
		Appointment testAppointment = new Appointment(TEN_LENGTH_INPUT, getTodayPlusDays(1), VALID_DESCRIPTION);
		
		Assertions.assertEquals(TEN_LENGTH_INPUT, testAppointment.getId());	
	}
	
	@Test
	public void testId_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Appointment(null, getTodayPlusDays(1), VALID_DESCRIPTION));
	}		
	
	@Test
	public void testId_withMoreThanMaxLength_throwsIllegalArgumentException() {	
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Appointment(TEN_LENGTH_INPUT + "A", getTodayPlusDays(1), VALID_DESCRIPTION));
	}
	
	@Test
	public void testId_withEmptyValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Appointment("", getTodayPlusDays(1), VALID_DESCRIPTION));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test date
	/////////////////////////////////////////////////////////////
	
	// Each test type is run once for the appointment constructor and once for the public setter method.
	@Test
	public void testDate_withFutureDate_isValid() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
		
		Assertions.assertEquals(getTodayPlusDays(1), testAppointment.getDate());		
	}
	
	@Test
	public void testSetDate_withFutureDate_isValid() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
		testAppointment.setDate(getTodayPlusDays(2));
		
		Assertions.assertEquals(getTodayPlusDays(2), testAppointment.getDate());
	}	
	
	@Test
	public void testDate_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Appointment(VALID_ID, null, VALID_DESCRIPTION));
	}	
	
	@Test
	public void testSetDate_withNullValue_throwsIllegalArgumentException() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testAppointment.setDate(null));
	}
	
	@Test
	public void testDate_withPastDate_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Appointment(VALID_ID, getPastDate(), VALID_DESCRIPTION));	
	}
	
	@Test
	public void testSetDate_withPastDate_throwsIllegalArgumentException() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testAppointment.setDate(getPastDate()));
	}
	
    @Test
    public void testDate_withTodaysDate_isValid() {
        Date today = new Date();
        Appointment testAppointment = new Appointment(VALID_ID, today, VALID_DESCRIPTION);
        
        Assertions.assertEquals(today, testAppointment.getDate());
    }
	
    @Test
    public void testSetDate_withTodaysDate_isValid() {
    	Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
    	Date today = new Date();
        testAppointment.setDate(today);
        
        Assertions.assertEquals(today, testAppointment.getDate());
    }
    
	/////////////////////////////////////////////////////////////
	/// Test description
	/////////////////////////////////////////////////////////////
	
	// Each test type is run once for the appointment constructor and once for the public setter method.
	@Test
	public void testDescription_withMinLength_isValid() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
		
		Assertions.assertEquals(VALID_DESCRIPTION, testAppointment.getDescription());		
	}
	
	@Test
	public void testSetDescription_withMinLength_isValid() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), TEN_LENGTH_INPUT);
		testAppointment.setDescription(VALID_DESCRIPTION);
		
		Assertions.assertEquals(VALID_DESCRIPTION, testAppointment.getDescription());
	}
	
	@Test
	public void testDescription_withMaxLength_isValid() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), FIFTY_LENGTH_INPUT);
		
		Assertions.assertEquals(FIFTY_LENGTH_INPUT, testAppointment.getDescription());	
	}
	
	@Test
	public void testSetDescription_withMaxLength_isValid() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
		testAppointment.setDescription(FIFTY_LENGTH_INPUT);
		
		Assertions.assertEquals(FIFTY_LENGTH_INPUT, testAppointment.getDescription());
	}
	
	@Test
	public void testDescription_withNullValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Appointment(VALID_ID, getTodayPlusDays(1), null));
	}	
	
	@Test
	public void testSetDescription_withNullValue_throwsIllegalArgumentException() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testAppointment.setDescription(null));
	}
	
	@Test
	public void testDescription_withMoreThanMaxLength_throwsIllegalArgumentException() {	
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Appointment(VALID_ID, getTodayPlusDays(1), FIFTY_LENGTH_INPUT + "A"));
	}
	
	@Test
	public void testSetDescription_withMoreThanMaxLength_throwsIllegalArgumentException() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testAppointment.setDescription(FIFTY_LENGTH_INPUT + "A"));
	}
	
	@Test
	public void testDescription_withEmptyValue_throwsIllegalArgumentException() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> new Appointment(VALID_ID, getTodayPlusDays(1), ""));
	}
	
	@Test
	public void testSetDescription_withEmptyValue_throwsIllegalArgumentException() {
		Appointment testAppointment = new Appointment(VALID_ID, getTodayPlusDays(1), VALID_DESCRIPTION);
	
		Assertions.assertThrows(IllegalArgumentException.class, () -> testAppointment.setDescription(""));
	}
}

