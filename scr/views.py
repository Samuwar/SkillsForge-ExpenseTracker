from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import func
from . import db
from .models import Expense
import json
import csv


views = Blueprint("views", __name__)
expense_category = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment')
    ]
current_expense = []

@views.route("/")
@views.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        # CHECK IF USER POST
        if request.method == 'POST':
            data = request.form
            category = data.get('category')
            amt_less_than = data.get('amt_less_than')
            amt_greater_than = data.get('amt_greater_than')
            payment_method = data.get('payment_method')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            
            # Initiate query            # 
            query = Expense.query
            query = query.filter_by(user_id=current_user.id)
            
            if category is not None and category != '':
                query = query.filter_by(category=category)
            if amt_less_than is not None and amt_less_than != '':
                query = query.filter(Expense.amount < amt_less_than)
            if amt_greater_than is not None and amt_greater_than != '':
                query = query.filter(Expense.amount > amt_greater_than)
            if payment_method is not None and payment_method != '':
                query = query.filter_by(payment_method=payment_method)
            if start_date is not None:
                print(start_date)
                query = query.filter(Expense.date_created >= start_date)
            if end_date is not None:
                query = query.filter(Expense.date_created <= end_date)
                
        # ON LOAD HOME    
        else:        
            query = Expense.query.filter_by(user_id=current_user.id)
            
        expenses = query.all()
        exp_json  = [expense.to_dict() for expense in expenses]
        current_expense.clear()
        current_expense.extend(exp_json)
        total_amount = sum(expense.amount for expense in expenses)
        summary_query = query.with_entities(Expense.category, func.sum(Expense.amount)).group_by(Expense.category)
        
        cat_summary = summary_query.all()
        
        return render_template("home.html", user=current_user, expenses=expenses, total_amount=total_amount, expense_category=expense_category, cat_summary=cat_summary, exp_json=exp_json)
    return render_template("home.html", user=current_user)


@login_required
@views.route('/create_expense', methods=['GET', 'POST'])
def create_expense():
    if request.method == 'POST':
        data = request.form
        title=data.get('title')
        amount=data.get('amount')
        category=data.get('category')
        payment_method=data.get('payment_method')
        user_id=current_user.id
        
        new_expense = Expense(title=title, amount=amount, category=category, payment_method=payment_method, user_id=user_id)
        db.session.add(new_expense)
        db.session.commit()
        flash("Expense Added Successfully")
        return redirect(url_for('views.home'))
        
    return render_template("create_expense.html", user=current_user)

@views.route("/update_expense/<int:id>", methods=['GET', 'POST'])
def update_expense(id):
    expense = Expense.query.get(id)
    if request.method == 'POST':
        data = request.form
        expense.title=data.get('title')
        expense.amount=data.get('amount')
        expense.category=data.get('category')
        expense.payment_method=data.get('payment_method')
        db.session.commit()
        flash('Expense updated successfully!')
        return redirect(url_for('views.home'))
    
    return render_template("/update_expense.html", user=current_user, expense=expense)

@views.route('/delete_expense/<int:id>', methods=['GET', 'POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        try:
            db.session.delete(expense)
            db.session.commit()
            return redirect(url_for(views.home))
            
        except Exception as e:
            db.session.rollback()
            flash("An error occured while deleting!")
    
    return render_template('delete_expense.html', expense=expense, user=current_user)


@views.route('/to_json')
def to_json():
    data = current_expense
    for x in data:
        x['date_created'] = str(x.get('date_created'))
        print(x)
    try:
        with open("expense.json", 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            flash('expense.json exported successfully!')
    except Exception as e:
        flash(f"an error occured! {e}", category='error')
    return redirect(url_for('views.home'))

@views.route('/to_csv')
def to_csv():
    print(current_user.username)
    data = current_expense
    fields = data[0].keys()
    for x in data:
        x['date_created'] = str(x.get('date_created'))
    try:
        with open("expense.csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
            flash('expense.json exported successfully!')
    except Exception as e:
        flash(f"an error occured! {e}", category='error')
    
    return redirect(url_for('views.home'))


        
        
        