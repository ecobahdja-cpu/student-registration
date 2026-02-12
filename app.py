from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
CSV_FILE = 'students.csv'

# إنشاء ملف CSV إذا لم يكن موجودًا
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'last_name', 'first_name', 'class', 'group', 'phone'])

# الصفحة الرئيسية - نموذج تسجيل التلاميذ
@app.route('/')
def home():
    return render_template('form.html')

# حفظ البيانات في CSV
@app.route('/submit', methods=['POST'])
def submit():
    last_name = request.form['last_name']
    first_name = request.form['first_name']
    class_name = request.form['class']
    group_name = request.form['group']
    phone = request.form['phone']

    # قراءة آخر id لإعطاء رقم تسلسلي
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)
        last_id = int(rows[-1][0]) if rows else 0
        new_id = last_id + 1

    # إضافة الصف الجديد
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([new_id, last_name, first_name, class_name, group_name, phone])

    return redirect('/')

# لوحة الإدارة - عرض التلاميذ
@app.route('/admin')
def admin():
    students = []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            students.append(row)

    # ترتيب حسب القسم ثم الفوج
    students.sort(key=lambda x: (x[3], x[4]))
    return render_template('admin.html', students=students)
