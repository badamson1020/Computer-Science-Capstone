package edu.snhu.badamson.contact;

import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public class Contact {
	
	private String id;
	private String firstName; 
	private String lastName;
	private String number; 
	private String address;

	public Contact(String id, String firstName, String lastName, String number, String address) {
		setId(id);
		setFirstName(firstName);
		setLastName(lastName);
		setNumber(number);
		setAddress(address);
	}

	public String getId() {
		return id;
	}

	private void setId(String id) {
		
		if (id == null) {
			throw new IllegalArgumentException("ID cannot be null.");
		}
		else if (id.length() > 10) {
			throw new IllegalArgumentException("ID cannot exceed 10 characters in length.");
		}
		else if (id.isEmpty()) {
			throw new IllegalArgumentException("ID must be at least 1 character in length.");
		}
		
		this.id = id;
	}

	public String getFirstName() {
		return firstName;
	}

	public void setFirstName(String firstName) {
		
		if (firstName == null) {
			throw new IllegalArgumentException("First name cannot be null.");
		}
		else if (firstName.length() > 10) {
			throw new IllegalArgumentException("First name cannot exceed 10 characters in length.");
		}
		else if (firstName.isEmpty()) {
			throw new IllegalArgumentException("First name must be at least 1 character in length.");
		}
		
		this.firstName = firstName;
	}

	public String getLastName() {
		return lastName;
	}

	public void setLastName(String lastName) {
		
		if (lastName == null) {
			throw new IllegalArgumentException("Last name cannot be null.");
		}
		else if (lastName.length() > 10) {
			throw new IllegalArgumentException("Last name cannot exceed 10 characters in length.");
		}
		else if (lastName.isEmpty()) {
			throw new IllegalArgumentException("Last name must be at least 1 character in length.");
		}
		
		this.lastName = lastName;
	}

	public String getNumber() {
		return number;
	}

	public void setNumber(String number) {
		
		if (number == null) {
			throw new IllegalArgumentException("Number cannot be null.");
		}
		else if (number.length() != 10) {
			throw new IllegalArgumentException("Number must be exactly 10 characters in length.");
		}
		
		this.number = number;
	}

	public String getAddress() {
		return address;
	}

	public void setAddress(String address) {
		
		if (address == null) {
			throw new IllegalArgumentException("Address cannot be null.");
		}
		else if (address.length() > 30) {
			throw new IllegalArgumentException("Address cannot exceed 30 characters in length.");
		}
		else if (address.isEmpty()) {
			throw new IllegalArgumentException("Address must be at least 1 character in length.");
		}
		
		this.address = address;
	}
}

