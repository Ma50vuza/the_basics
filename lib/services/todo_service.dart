import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/todo.dart';
import 'auth_service.dart';

class TodoService {
  static const String baseUrl =
      'https://todo-backend-liyx.onrender.com/api/todo_entries';

  // GET all todos for logged in user
  static Future<List<Todo>> getAllTodos() async {
    try {
      final response =
          await http.get(Uri.parse(baseUrl), headers: AuthService.headers);

      if (response.statusCode == 200) {
        List<dynamic> body = jsonDecode(response.body);
        return body.map((dynamic item) => Todo.fromJson(item)).toList();
      } else if (response.statusCode == 401) {
        throw Exception('Unauthorized: Please login again');
      } else {
        throw Exception('Failed to load todos: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  // POST create todo
  static Future<Todo> createTodo(String name) async {
    try {
      final response = await http.post(
        Uri.parse(baseUrl),
        headers: AuthService.headers,
        body: jsonEncode({'name': name}),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        Map<String, dynamic> body = jsonDecode(response.body);
        return Todo.fromJson(body);
      } else if (response.statusCode == 401) {
        throw Exception('Unauthorized: Please login again');
      } else {
        throw Exception('Failed to create todo: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  // PUT update todo
  static Future<Todo> updateTodo(String id, String name) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/$id'),
        headers: AuthService.headers,
        body: jsonEncode({'name': name}),
      );

      if (response.statusCode == 200) {
        Map<String, dynamic> body = jsonDecode(response.body);
        return Todo.fromJson(body);
      } else if (response.statusCode == 401) {
        throw Exception('Unauthorized: Please login again');
      } else {
        throw Exception('Failed to update todo: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  // DELETE todo
  static Future<String> deleteTodo(String id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/$id'),
        headers: AuthService.headers,
      );

      if (response.statusCode == 200) {
        Map<String, dynamic> body = jsonDecode(response.body);
        return body['message'] ?? 'Todo deleted successfully';
      } else if (response.statusCode == 401) {
        throw Exception('Unauthorized: Please login again');
      } else {
        throw Exception('Failed to delete todo: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
}
