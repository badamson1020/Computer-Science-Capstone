package edu.snhu.badamson.task;

import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import lombok.EqualsAndHashCode;

public class TaskService {
	private List<Task> tasks;
	
	public TaskService() {
		tasks = new ArrayList<>();			
	}

	/**
	 * Adds a new task to the service
	 * Checks that the ID is unique
	 * @param newTask is the task to add
	 * @throws IllegalArgumentException if the task is null or a duplicate ID.
	 */
	public void add(Task newTask) {
		 if (newTask == null) {
	            throw new IllegalArgumentException("Task cannot be null.");
		 }
		
		boolean isDuplicate = false;
		for (Task task: tasks) {
			if (task.getId().equals(newTask.getId())) {
				isDuplicate = true;
				break;
			}
		}
		
		if (isDuplicate) {
			throw new IllegalArgumentException("Cannot add task with duplicate ID: " + newTask.getId());
		}
		tasks.add(newTask);		
	}
	
	/**
	 * Deletes a task by its ID.
	 * @param id The ID of the task to be deleted.
	 * @throws IllegalArgumentException if the ID is null.
	 * @throws NoSuchElementException if no task with the given ID exists.
	 */
	public void delete(String id) {
	    if (id == null) {
	        throw new IllegalArgumentException("ID cannot be null.");
	    }
	    
	    Task taskToDelete = null;
	    
	    for (Task task : tasks) {
	        if (task.getId().equals(id)) {
	            taskToDelete = task;
	            break;
	        }
	    }
	    
	    if (taskToDelete == null) {
	        throw new NoSuchElementException("Task with ID " + id + " does not exist.");
	    }
	    
	    tasks.remove(taskToDelete);
	}
	
	/**
	 * Updates an existing task, ID cannot be updated. 
	 * @param updatedTask The task with updated fields.
     * @throws IllegalArgumentException if the task or its ID are null.
     * @throws NoSuchElementException if no task with the ID exists.
	 */
	public void edit(Task updatedTask) {
		if (updatedTask == null || updatedTask.getId() == null) {
	        throw new IllegalArgumentException("The task and/or its ID cannot be null.");
	    }
	    
	    Task existingTask = get(updatedTask.getId());
	    
	    if (existingTask == null) {
	        throw new NoSuchElementException("Task with ID " + updatedTask.getId() + " does not exist.");
	    }
	    
	    existingTask.setName(updatedTask.getName());
	    existingTask.setDescription(updatedTask.getDescription());
	}
	
	/**
	 * Get the task by ID.
	 * Returns the task if found, otherwise returns null.
	 * @param id - the task ID.
	 * @return the task or null if ID does not exist.
	 * @throws IllegalArgumentException if the ID is null.
	 */
	public Task get(String id) {
		if (id == null) {
	        throw new IllegalArgumentException("ID cannot be null.");
	    }
		
		Task foundTask = null;
		
		for (Task task: tasks) {
			if(task.getId().equals(id)) {
				foundTask = task;
				break;
			}
		}
		return foundTask;
	}
	
	/**
	 * Gets a copy of the list of tasks, preventing changes to the internal task list.
	 * Returns an empty list if none exists.
	 * @return - the list of tasks or none if it is empty.
	 */
	public List<Task> getAll() {
	    List<Task> taskCopy = new ArrayList<>(tasks);
	    
	    return taskCopy;	    
	}
}
