class Todo {
  final String id;
  final String name;
  final String userId;

  Todo({required this.id, required this.name, required this.userId});

  factory Todo.fromJson(Map<String, dynamic> json) {
    return Todo(
      id: json['id'],
      name: json['name'],
      userId: json['userId'] ?? json['user_id'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {'id': id, 'name': name, 'userId': userId};
  }
}
