package edu.snhu.badamson.appointment;

import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.NoSuchElementException;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public class AppointmentServiceTest {
	
	private AppointmentService service;
	
	 // Method used to create new future dates for testing.
    private Date getTodayPlusDays(int days) {
        Calendar cal = Calendar.getInstance();
        cal.add(Calendar.DATE, days);
        return cal.getTime();
    }
	
	@BeforeEach
	public void setup() {
		service = new AppointmentService();		
	}	
	
	/////////////////////////////////////////////////////////////
	/// Test Add
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testAdd_withNewElement_successfullyAdds() {
		Appointment newAppointment = new Appointment("32", getTodayPlusDays(1), "Meet with new contact");
		
		service.add(newAppointment);
		
		Assertions.assertEquals(service.get(newAppointment.getId()), newAppointment);
	}
	
	@Test
	public void testAdd_withDuplicateElement_throwsIllegalArgumentException() {
		Appointment newAppointment = new Appointment("32", getTodayPlusDays(1), "Meet with new contact");
		
		service.add(newAppointment);
		
		Assertions.assertNotNull(service.get(newAppointment.getId()));	
		
		Assertions.assertThrows(IllegalArgumentException.class, () -> service.add(newAppointment));

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
		Appointment newAppointment = new Appointment("32", getTodayPlusDays(1), "Meet with new contact");
		
		service.add(newAppointment);
		
		Assertions.assertNotNull(service.get(newAppointment.getId())); 
	    
	    service.delete(newAppointment.getId()); 
	    
	    Assertions.assertNull(service.get(newAppointment.getId())); 
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
	/// Test Get
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testGet_withValidId_returnsCorrectAppointment() {
		Appointment newAppointment = new Appointment("32", getTodayPlusDays(1), "Meet with new contact");
	    service.add(newAppointment);

	    Appointment selectedAppointment = service.get(newAppointment.getId());
	        
	    Assertions.assertNotNull(selectedAppointment);
	    Assertions.assertEquals(newAppointment, selectedAppointment); 
	}

	@Test
	public void testGet_withInvalidId_returnsNull() {		
		Appointment newAppointment = new Appointment("32", getTodayPlusDays(1), "Meet with new contact");
	    service.add(newAppointment);
		
	    Appointment selectedAppointment = service.get("234");
	        
	    Assertions.assertNull(selectedAppointment);
	}

	@Test
	public void testGet_withNullId_throwsIllegalArgumentException() {
	    Assertions.assertThrows(IllegalArgumentException.class, () -> service.get(null));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test GetAll
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testGetAll_withMultipleAppointments_returnsAllAppointments() {
		Appointment appointment1 = new Appointment("32", getTodayPlusDays(1), "Meet with new contact");
		Appointment appointment2 = new Appointment("2", getTodayPlusDays(3), "Discuss new business plans");
	    service.add(appointment1);
	    service.add(appointment2);
	    
	    List<Appointment> allAppointments = service.getAll();
	    
	    Assertions.assertEquals(2, allAppointments.size());
	    Assertions.assertTrue(allAppointments.contains(appointment1));
	    Assertions.assertTrue(allAppointments.contains(appointment2));
	}
	
	@Test
	public void testGetAll_withNoAppointments_returnsEmptyList() {
	    List<Appointment> allAppointments = service.getAll();
	    
	    Assertions.assertTrue(allAppointments.isEmpty());
	}
	
	@Test
	public void testGetAll_afterDeletingAppointment_returnsRemainingAppointments() {
		Appointment appointment1 = new Appointment("32", getTodayPlusDays(1), "Meet with new contact");
		Appointment appointment2 = new Appointment("2", getTodayPlusDays(3), "Discuss new business plans");
	    service.add(appointment1);
	    service.add(appointment2);
	    
	    service.delete(appointment1.getId());
	    
	    List<Appointment> allAppointments = service.getAll();
	    
	    Assertions.assertEquals(1, allAppointments.size());
	    Assertions.assertTrue(allAppointments.contains(appointment2));
	    Assertions.assertFalse(allAppointments.contains(appointment1));
	}	
}
