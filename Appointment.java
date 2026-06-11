package edu.snhu.badamson.appointment;

import java.util.Date;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public class Appointment {

	private String id;
	private Date date; 
	private String description;

	public Appointment(String id, Date date, String description) {
		setId(id);
		setDate(date);
		setDescription(description);
	}
	
	// Constructor allows for testing that compares the appointment objects, instead of comparing their references.
	public Appointment(Appointment copyAppointment) {
		this(copyAppointment.id, new Date(copyAppointment.date.getTime()), copyAppointment.description);
	}

	public String getId() {
		return id;
	}

	private void setId(String id) {
		if (id == null) {
			throw new IllegalArgumentException("ID cannot be null.");
		}
		else if (id.length() > 10) {
			throw new IllegalArgumentException("ID cannot exeed 10 characters in length.");
		}
		else if (id.isEmpty()) {
			throw new IllegalArgumentException("ID must be at least 1 character in length.");
		}
		
		this.id = id;
	}

	public Date getDate() {
		return new Date(date.getTime());
	}

	public void setDate(Date date) {
		if (date == null) {
			throw new IllegalArgumentException("Date cannot be null.");	
		}
		
	    Date now = new Date();

	    if (date.before(now)) {
	        throw new IllegalArgumentException("Date and time cannot be in the past.");
	    }

	    this.date = new Date(date.getTime()); 
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		if (description == null) {
			throw new IllegalArgumentException("Description cannot be null.");
		}
		else if (description.length() > 50) {
			throw new IllegalArgumentException("Description cannot exeed 50 characters in length.");
		}
		else if (description.isEmpty()) {
			throw new IllegalArgumentException("Description must be at least 1 character in length.");
		}
		
		this.description = description;
	}
}
