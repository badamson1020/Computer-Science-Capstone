package edu.snhu.badamson.appointment;

import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public class AppointmentService {
	private List<Appointment> appointments;
	
	public AppointmentService() {
		appointments = new ArrayList<>();			
	}

	/**
	 * Adds a new appointment to the service
	 * Checks that the ID is unique
	 * @param newAppointment is the appointment to add
	 * @throws IllegalArgumentException if the appointment is null or a duplicate ID.
	 */
	public void add(Appointment newAppointment) {
		 if (newAppointment == null) {
	            throw new IllegalArgumentException("Appointment cannot be null.");
		 }
		
		boolean isDuplicate = false;
		for (Appointment appointment : appointments) {
			if (appointment.getId().equals(newAppointment.getId())) {
				isDuplicate = true;
				break;
			}
		}
		
		if (isDuplicate) {
			throw new IllegalArgumentException("Cannot add appointment with duplicate ID: " + newAppointment.getId());
		}
		appointments.add(newAppointment);		
	}
	
	/**
	 * Deletes an appointment by its ID.
	 * @param id The ID of the appointment to be deleted.
	 * @throws IllegalArgumentException if the ID is null.
	 * @throws NoSuchElementException if no appointment with the given ID exists.
	 */
	public void delete(String id) {
	    if (id == null) {
	        throw new IllegalArgumentException("ID cannot be null.");
	    }
	    
	    Appointment appointmentToDelete = null;
	    
	    for (Appointment appointment : appointments) {
	        if (appointment.getId().equals(id)) {
	        	appointmentToDelete = appointment;
	            break;
	        }
	    }
	    
	    if (appointmentToDelete == null) {
	        throw new NoSuchElementException("Appointment with ID " + id + " does not exist.");
	    }
	    
	    appointments.remove(appointmentToDelete);
	}
	
	/**
	 * Get the appointment by ID.
	 * Returns the appointment if found, otherwise returns null.
	 * @param id - the appointment ID.
	 * @return the appointment or null if ID does not exist.
	 * @throws IllegalArgumentExcpetion if the ID is null.
	 */
	public Appointment get(String id) {
		if (id == null) {
	        throw new IllegalArgumentException("ID cannot be null.");
	    }
		
		Appointment foundAppointment = null;
		
		for (Appointment appointment : appointments) {
			if(appointment.getId().equals(id)) {
				foundAppointment = appointment;
				break;
			}
		}
		
		// A copy of the appointment is returned to allow for testing that compares different references of the appointment objects.
		Appointment copyAppointment = null;
		if (foundAppointment != null) {
			copyAppointment = new Appointment(foundAppointment);
		}
		
		return copyAppointment;
	}
	
	/**
	 * Gets a copy of the list of appointments, preventing changes to the internal appointment list.
	 * Returns an empty list if none exists.
	 * @return - the list of appointments or none if it is empty.
	 */
	public List<Appointment> getAll() {
	    List<Appointment> appointmentCopy = new ArrayList<>(appointments);
	    
	    return appointmentCopy;	    
	}
}
