import click
import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from property.database import init_db, SessionLocal
from property.models import Agent, Property, Room, Client, Payment
from datetime import datetime  # Import datetime module

init_db()


@click.group()
def cli():
    """Property Management CLI."""
    pass

@click.command()
@click.option('--name', prompt='Your name', help='Name of the agent.')
@click.option('--email', prompt='Your email', help='Email of the agent.')
@click.option('--password', prompt='Your password', hide_input=True, confirmation_prompt=True, help='Password of the agent.')
def signup(name, email, password):
    """Register a new agent."""
    db = SessionLocal()
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        agent = Agent(name=name, email=email, hashed_password=hashed_password)
        db.add(agent)
        db.commit()
        click.echo(f"Agent registered and logged in successfully as {name}!")
    except IntegrityError:
        db.rollback()
        click.echo("Email already exists. Please try a different email.")
    finally:
        db.close()
        
@click.command()
@click.option('--email', prompt='Your email', help='Email of the agent.')
@click.option('--password', prompt='Your password', hide_input=True, help='Password of the agent.')
def login(email, password):
    """Log in an existing agent."""
    db = SessionLocal()
    try:
        agent = db.query(Agent).filter(Agent.email == email).first()
        if agent and bcrypt.checkpw(password.encode('utf-8'), agent.hashed_password):
            click.echo(f"Logged in successfully as {agent.name}!")
        else:
            click.echo("Invalid email or password. Please try again.")
    finally:
        db.close()


@click.command()
@click.option('--address', prompt='Property address', help='Address of the property.')
@click.option('--location', prompt='Property location', help='Location of the property.')
@click.option('--agent_id', prompt='Agent ID', help='ID of the agent responsible for the property.', type=int)
def add_property(address, location, agent_id):
    """Add a new property."""
    db = SessionLocal()
    try:
        property = Property(address=address, location=location, agent_id=agent_id)
        db.add(property)
        db.commit()
        click.echo(f"Property at {address} added successfully!")
    except IntegrityError:
        db.rollback()
        click.echo("Failed to add property. Please check the provided details.")
    finally:
        db.close() 

@click.command()
@click.option('--name', prompt='Client name', help='Name of the client.')
@click.option('--email', prompt='Client email', help='Email of the client.')
@click.option('--password', prompt='Client password', hide_input=True, confirmation_prompt=True, help='Password of the client.')
@click.option('--agent_id', prompt='Agent ID', help='ID of the agent responsible for the client.', type=int)
@click.option('--property_id', prompt='Property ID', help='ID of the property associated with the client.', type=int)
def add_client(name, email, password, agent_id, property_id):
    """Add a new client."""
    db = SessionLocal()
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        client = Client(name=name, email=email, hashed_password=hashed_password, agent_id=agent_id, property_id=property_id)
        db.add(client)
        db.commit()
        click.echo(f"Client {name} added successfully!")
    except IntegrityError:
        db.rollback()
        click.echo("Failed to add client. Please check the provided details.")
    finally:
        db.close()

@click.command()
@click.option('--type', prompt='Room type', help='Type of the room.')
@click.option('--size', prompt='Room size', help='Size of the room.', type=float)
@click.option('--property_id', prompt='Property ID', help='ID of the property to which the room belongs.', type=int)
def add_room(type, size, property_id):
    """Add a new room to a property."""
    db = SessionLocal()
    try:
        room = Room(type=type, size=size, property_id=property_id)
        db.add(room)
        db.commit()
        click.echo(f"Room of type {type} with size {size} added successfully to property ID {property_id}!")
    except IntegrityError:
        db.rollback()
        click.echo("Failed to add room. Please check the provided details.")
    finally:
        db.close()  
@click.command()
@click.option('--amount', prompt='Payment amount', help='Amount of the payment.', type=float)
@click.option('--date', prompt='Payment date', help='Date of the payment (YYYY-MM-DD).')
@click.option('--client_id', prompt='Client ID', help='ID of the client making the payment.', type=int)
def add_payment(amount, date, client_id):
    """Add a new payment for a client."""
    db = SessionLocal()
    try:
        payment_date = datetime.strptime(date, '%Y-%m-%d').date()
        payment = Payment(amount=amount, date=payment_date, client_id=client_id)
        db.add(payment)
        db.commit()
        click.echo(f"Payment of {amount} on {payment_date} added successfully for client ID {client_id}!")
    except IntegrityError:
        db.rollback()
        click.echo("Failed to add payment. Please check the provided details.")
    finally:
        db.close()  

@click.command()
def list_clients():
    """List all clients."""
    db = SessionLocal()
    clients = db.query(Client).all()
    for client in clients:
        click.echo(f"Client ID: {client.id}, Name: {client.name}, Email: {client.email}")
    db.close()

@click.command()
def list_properties():
    """List all properties."""
    db = SessionLocal()
    properties = db.query(Property).all()
    for property in properties:
        click.echo(f"Property ID: {property.id}, Address: {property.address}, Location: {property.location}")
    db.close()

@click.command()
def list_rooms():
    """List all rooms."""
    db = SessionLocal()
    rooms = db.query(Room).all()
    for room in rooms:
        click.echo(f"Room ID: {room.id}, Type: {room.type}, Size: {room.size}, Property ID: {room.property_id}")
    db.close()

@click.command()
@click.option('--property_id', prompt='Property ID', help='ID of the property to update.', type=int)
@click.option('--new_address', prompt='New address', help='New address of the property.')
@click.option('--new_location', prompt='New location', help='New location of the property.')
def update_property(property_id, new_address, new_location):
    """Update an existing property."""
    db = SessionLocal()
    property = db.query(Property).filter(Property.id == property_id).first()
    if property:
        property.address = new_address
        property.location = new_location
        db.commit()
        click.echo(f"Property ID {property_id} updated successfully!")
    else:
        click.echo(f"Property ID {property_id} not found.")
    db.close()

@click.command()
@click.option('--client_id', prompt='Client ID', help='ID of the client to delete.', type=int)
def delete_client(client_id):
    """Delete an existing client."""
    db = SessionLocal()
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
        click.echo(f"Client ID {client_id} deleted successfully!")
    else:
        click.echo(f"Client ID {client_id} not found.")
    db.close()

@click.command()
@click.option('--property_id', prompt='Property ID', help='ID of the property to delete.', type=int)
def delete_property(property_id):
    """Delete an existing property."""
    db = SessionLocal()
    property = db.query(Property).filter(Property.id == property_id).first()
    if property:
        db.delete(property)
        db.commit()
        click.echo(f"Property ID {property_id} deleted successfully!")
    else:
        click.echo(f"Property ID {property_id} not found.")
    db.close()

@click.command()
@click.option('--room_id', prompt='Room ID', help='ID of the room to delete.', type=int)
def delete_room(room_id):
    """Delete an existing room."""
    db = SessionLocal()
    room = db.query(Room).filter(Room.id == room_id).first()
    if room:
        db.delete(room)
        db.commit()
        click.echo(f"Room ID {room_id} deleted successfully!")
    else:
        click.echo(f"Room ID {room_id} not found.")
    db.close()

@click.command()
@click.option('--name', prompt='Client name to search for', help='Name of the client to search.')
def search_client(name):
    """Search for clients by name."""
    db = SessionLocal()
    clients = db.query(Client).filter(Client.name.ilike(f"%{name}%")).all()
    if clients:
        for client in clients:
            click.echo(f"Client ID: {client.id}, Name: {client.name}, Email: {client.email}")
    else:
        click.echo(f"No clients found with name {name}.")
    db.close()

@click.command()
@click.option('--address', prompt='Property address to search for', help='Address of the property to search.')
def search_property(address):
    """Search for properties by address."""
    db = SessionLocal()
    properties = db.query(Property).filter(Property.address.ilike(f"%{address}%")).all()
    if properties:
        for property in properties:
            click.echo(f"Property ID: {property.id}, Address: {property.address}, Location: {property.location}")
    else:
        click.echo(f"No properties found with address {address}.")
    db.close()

@click.command()
@click.option('--client_id', prompt='Client ID', help='ID of the client to view payment history.', type=int)
def view_payments(client_id):
    """View payment history of a client."""
    db = SessionLocal()
    payments = db.query(Payment).filter(Payment.client_id == client_id).all()
    if payments:
        for payment in payments:
            click.echo(f"Payment ID: {payment.id}, Amount: {payment.amount}, Date: {payment.date}")
    else:
        click.echo(f"No payments found for client ID {client_id}.")
    db.close()

import csv

@click.command()
def export_property_report():
    """Export a report of all properties to a CSV file."""
    db = SessionLocal()
    properties = db.query(Property).all()
    with open('properties_report.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Property ID", "Address", "Location", "Agent ID"])
        for property in properties:
            writer.writerow([property.id, property.address, property.location, property.agent_id])
    click.echo("Property report exported successfully!")
    db.close()
            
cli.add_command(signup)
cli.add_command(login)
cli.add_command(add_property)
cli.add_command(add_client)
cli.add_command(add_room)
cli.add_command(add_payment)
cli.add_command(list_clients)
cli.add_command(list_properties)
cli.add_command(list_rooms)
cli.add_command(update_property)
cli.add_command(delete_client)
cli.add_command(delete_property)
cli.add_command(delete_room)
cli.add_command(search_client)
cli.add_command(search_property)
cli.add_command(view_payments)
cli.add_command(export_property_report)


if __name__ == '__main__':
    cli()
