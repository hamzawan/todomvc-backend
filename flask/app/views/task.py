from flask import request, jsonify, Blueprint, g
from common.services.task import TaskService
from app.helpers.decorators import login_required_blueprint
from app.helpers.response import get_success_response, get_failure_response
from common.app_config import config
from datetime import datetime

task_bp = Blueprint('task', __name__)

def parse_datetime(date_string):
    if not date_string:
        return None
    try:
        if date_string.endswith('Z'):
            date_string = date_string[:-1] + '+00:00'
        return datetime.fromisoformat(date_string)
    except ValueError:
        return None

def format_task_response(task):
    return {
        'id': task.entity_id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'assigned_to_id': task.assigned_to_id,
        'organization_id': task.organization_id,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'created_at': task.changed_on.isoformat() if task.changed_on else None,
        'updated_at': task.changed_on.isoformat() if task.changed_on else None,
        'version': task.version,
        'active': task.active
    }

@task_bp.route('/create', methods=['POST'])
@login_required_blueprint()
def create_task(person=None):
    """Create a new task for the authenticated user"""
    data = request.json or {}
    
    if not data.get('title'):
        return jsonify({'success': False, 'message': 'Title is required'}), 400
    
    title = data.get('title')
    description = data.get('description', '')
    priority = data.get('priority', 'medium')
    due_date = parse_datetime(data.get('due_date'))
    
    user_id = g.person.entity_id
    
    try:
        task_service = TaskService(config)
        task = task_service.create_task(
            title=title,
            description=description,
            assigned_to_id=user_id,
            priority=priority,
            organization_id=data.get('organization_id'),
            due_date=due_date
        )
        
        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'task': format_task_response(task)
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@task_bp.route('/list', methods=['GET'])
@login_required_blueprint()
def list_tasks(person=None):
    """Get all tasks for the authenticated user with optional status and priority filtering"""
    user_id = g.person.entity_id
    
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    title = request.args.get('title', '')
    
    try:
        task_service = TaskService(config)
        tasks = task_service.get_tasks_by_user(user_id, status_filter, priority_filter, title)
        
        task_list = [format_task_response(task) for task in tasks]
        
        return jsonify({
            'success': True,
            'tasks': task_list,
            'count': len(task_list),
            'filters': {
                'status': status_filter,
                'priority': priority_filter
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@task_bp.route('/<string:task_id>', methods=['GET'])
@login_required_blueprint()
def get_task(task_id, person=None):
    """Get a specific task by ID"""
    user_id = g.person.entity_id
    
    try:
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id, user_id)
        
        if not task:
            return jsonify({'success': False, 'message': 'Task not found'}), 404
        
        return jsonify({
            'success': True,
            'task': format_task_response(task)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@task_bp.route('/<string:task_id>', methods=['PUT'])
@login_required_blueprint()
def update_task(task_id, person=None):
    """Update a specific task"""
    user_id = g.person.entity_id
    data = request.json or {}
    
    try:
        task_service = TaskService(config)
        due_date = parse_datetime(data.get('due_date')) if 'due_date' in data else None
        task = task_service.update_task(
            task_id=task_id,
            user_id=user_id,
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status'),
            priority=data.get('priority', 'medium'),
            due_date=due_date
        )
        
        if not task:
            return jsonify({'success': False, 'message': 'Task not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Task updated successfully',
            'task': format_task_response(task)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@task_bp.route('/<string:task_id>/toggle-status', methods=['PATCH'])
@login_required_blueprint()
def toggle_task_status(task_id, person=None):
    """Toggle task completion status between completed and pending"""
    user_id = g.person.entity_id
    
    try:
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id, user_id)
        
        if not task:
            return jsonify({'success': False, 'message': 'Task not found'}), 404
        
        new_status = 'completed' if task.status != 'completed' else 'incomplete'
        
        updated_task = task_service.update_task(
            task_id=task_id,
            user_id=user_id,
            status=new_status
        )
        
        return jsonify({
            'success': True,
            'message': f'Task marked as {new_status}',
            'task': format_task_response(updated_task)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@task_bp.route('/<string:task_id>', methods=['DELETE'])
@login_required_blueprint()
def delete_task(task_id, person=None):
    """Delete a specific task"""
    user_id = g.person.entity_id
    
    try:
        task_service = TaskService(config)
        success = task_service.delete_task(task_id, user_id)
        
        if not success:
            return jsonify({'success': False, 'message': 'Task not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
