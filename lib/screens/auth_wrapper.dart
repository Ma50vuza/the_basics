import 'package:flutter/material.dart';
import '../../services/auth_service.dart';
import 'login.dart';
import '../screens/todo_screen.dart';

class AuthWrapper extends StatelessWidget {
  const AuthWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return AuthService.isLoggedIn() ? const TodoScreen() : const LoginScreen();
  }
}
