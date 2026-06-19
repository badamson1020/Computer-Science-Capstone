package edu.snhu.badamson.task;

import lombok.EqualsAndHashCode;

public class Task {
	
	private String id;
	private String name; 
	private String description;

	public Task(String id, String name, String description) {
		setId(id);
		setName(name);
		setDescription(description);
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

	public String getName() {
		return name;
	}

	public void setName(String name) {
		if (name == null) {
			throw new IllegalArgumentException("Name cannot be null.");
		}
		else if (name.length() > 20) {
			throw new IllegalArgumentException("Name cannot exceed 20 characters in length.");
		}
		else if (name.isEmpty()) {
			throw new IllegalArgumentException("Name must be at least 1 character in length.");
		}
		
		this.name = name;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		if (description == null) {
			throw new IllegalArgumentException("Description cannot be null.");
		}
		else if (description.length() > 50) {
			throw new IllegalArgumentException("Description cannot exceed 50 characters in length.");
		}
		else if (description.isEmpty()) {
			throw new IllegalArgumentException("Description must be at least 1 character in length.");
		}
		
		this.description = description;
	}
}
