import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user.dart';

class AuthService {
  static const String baseUrl = 'https://todo-backend-liyx.onrender.com';
  static String? _token;

  static String? get token => _token;

  static Map<String, String> get headers => {
        'Content-Type': 'application/json',
        if (_token != null) 'Authorization': 'Bearer $_token',
      };

  // Register
  static Future<Map<String, dynamic>> register(String username, String email,
      String password, String verifyPassword) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'email': email, // Assuming username is used as email
          'password': password,
          'verify_password': verifyPassword,
        }),
      );

      final body = jsonDecode(response.body);

      if (response.statusCode == 200 || response.statusCode == 201) {
        return {
          'success': true,
          'message': body['message'] ?? 'Registration successful'
        };
      } else {
        return {
          'success': false,
          'message': body['message'] ?? 'Registration failed'
        };
      }
    } catch (e) {
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  // Login
  static Future<Map<String, dynamic>> login(
      String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
        }),
      );

      final body = jsonDecode(response.body);

      if (response.statusCode == 200) {
        // Store the token from access_token field
        _token = body['access_token'];
        return {
          'success': true,
          'token': _token,
          'message': 'Login successful'
        };
      } else {
        return {'success': false, 'message': body['message'] ?? 'Login failed'};
      }
    } catch (e) {
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  // Logout
  static Future<void> logout() async {
    _token = null;
  }

  // Check if user is logged in
  static bool isLoggedIn() {
    return _token != null;
  }

  // Get current user (you'll need to check if this endpoint exists)
  static Future<User?> getCurrentUser() async {
    if (!isLoggedIn()) return null;

    try {
      // This endpoint might not exist - check your API documentation
      final response = await http.get(
        Uri.parse('$baseUrl/api/user/me'), // Updated endpoint path
        headers: headers,
      );

      if (response.statusCode == 200) {
        final body = jsonDecode(response.body);
        return User.fromJson(body);
      }
    } catch (e) {
      print('Error getting current user: $e');
    }
    return null;
  }

  // Optional: Method to validate token
  static Future<bool> validateToken() async {
    if (!isLoggedIn()) return false;

    try {
      // You might want to add a token validation endpoint
      final response = await http.get(
        Uri.parse('$baseUrl/api/validate-token'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return true;
      } else {
        // Token is invalid, clear it
        _token = null;
        return false;
      }
    } catch (e) {
      print('Error validating token: $e');
      return false;
    }
  }
}
