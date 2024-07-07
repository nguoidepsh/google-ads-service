# models/__init__.py
from .ticket_model import Ticket, TicketCreate, TicketRead, TicketPatch
from .task_model import Task, Task, TaskCreate, TaskRead, TaskPatch

Ticket.update_forward_refs()
Task.update_forward_refs()