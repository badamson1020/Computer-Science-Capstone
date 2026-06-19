package edu.snhu.badamson.task;

import java.util.List;
import java.util.NoSuchElementException;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import lombok.EqualsAndHashCode;

public class TaskServiceTest {
	
	private TaskService service;
	
	@BeforeEach
	public void setup() {
		service = new TaskService();		
	}	
	
	/////////////////////////////////////////////////////////////
	/// Test Add
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testAdd_withNewElement_successfullyAdds() {
		Task newTask = new Task("32", "Clean", "Removes junk data");
		
		service.add(newTask);
		
		Assertions.assertEquals(service.get(newTask.getId()), newTask);
	}
	
	@Test
	public void testAdd_withDuplicateElement_throwsIllegalArgumentException() {
		Task newTask = new Task("32", "Clean", "Removes junk data");
		
		service.add(newTask);
		
		Assertions.assertNotNull(service.get(newTask.getId()));	
		
		Assertions.assertThrows(IllegalArgumentException.class, () -> service.add(newTask));

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
		Task newTask = new Task("32", "Clean", "Removes junk data");
		
		service.add(newTask);
		
		Assertions.assertNotNull(service.get(newTask.getId())); 
	    
	    service.delete(newTask.getId()); 
	    
	    Assertions.assertNull(service.get(newTask.getId())); 
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
	public void testEdit_withUpdatedTask_updatesFieldsSuccessfully() {
	    Task newTask = new Task("32", "Clean", "Removes junk data");
	    service.add(newTask);

	    Task updatedTask = new Task("32", "Compress", "Compresses files");
	    service.edit(updatedTask);

	    Task checkedTask = service.get("32");

	    Assertions.assertEquals("Compress", checkedTask.getName());
	    Assertions.assertEquals("Compresses files", checkedTask.getDescription());
	}
	
	@Test
	public void testEdit_withNonExistingTask_throwsNoSuchElementException() {
	    // A new task is created, but never added to the TaskService.
	    Task newTask = new Task("123", "Non", "Existent");

	    Assertions.assertThrows(NoSuchElementException.class, () -> service.edit(newTask));
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
	    Task newTask = new Task("32", "Clean", "Removes junk data");
	    service.add(newTask);

	    Task selectedTask = service.get(newTask.getId());
	        
	    Assertions.assertNotNull(selectedTask);
	    Assertions.assertEquals(newTask, selectedTask); 
	}

	@Test
	public void testGet_withInvalidId_returnsNull() {		
		Task newTask = new Task("32", "Clean", "Removes junk data");
	    service.add(newTask);
		
		Task selectedTask = service.get("234");
	        
	    Assertions.assertNull(selectedTask);
	}

	@Test
	public void testGet_withNullId_throwsIllegalArgumentException() {
	    Assertions.assertThrows(IllegalArgumentException.class, () -> service.get(null));
	}
	
	/////////////////////////////////////////////////////////////
	/// Test GetAll
	/////////////////////////////////////////////////////////////
	
	@Test
	public void testGetAll_withMultipleTasks_returnsAllTasks() {
	    Task task1 = new Task("32", "Clean", "Removes junk data");
	    Task task2 = new Task("12", "Compress", "Compresses files");
	    service.add(task1);
	    service.add(task2);
	    
	    List<Task> allTasks = service.getAll();
	    
	    Assertions.assertEquals(2, allTasks.size());
	    Assertions.assertTrue(allTasks.contains(task1));
	    Assertions.assertTrue(allTasks.contains(task2));
	}
	
	@Test
	public void testGetAll_withNoTasks_returnsEmptyList() {
	    List<Task> allTasks = service.getAll();
	    
	    Assertions.assertTrue(allTasks.isEmpty());
	}
	
	@Test
	public void testGetAll_afterDeletingTask_returnsRemainingTasks() {
	    Task task1 = new Task("32", "Clean", "Removes junk data");
	    Task task2 = new Task("12", "Compress", "Compresses files");
	    service.add(task1);
	    service.add(task2);
	    
	    service.delete(task1.getId());
	    
	    List<Task> allTasks = service.getAll();
	    
	    Assertions.assertEquals(1, allTasks.size());
	    Assertions.assertTrue(allTasks.contains(task2));
	    Assertions.assertFalse(allTasks.contains(task1));
	}	
}
