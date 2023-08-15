from django.shortcuts import render, redirect
from .models import KpiModel, SportModel, EvrikaModel, BookModel, WorkModel, BookItem, DeadlineModel, MeetingModel, \
    MeetingDateModel, SportDateModel
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.

def index(request):
    kpi_models = KpiModel.objects.all().order_by('-created_at')
    result = []
    for x in kpi_models:
        books = sum(x.score for x in BookModel.objects.filter(kpi=x))
        sports = sum(x.score for x in SportModel.objects.filter(kpi=x))
        evrikas = sum(x.score for x in EvrikaModel.objects.filter(kpi=x))
        works = sum(float(x.score) for x in WorkModel.objects.filter(kpi=x))
        meetings = sum(x.score for x in MeetingModel.objects.filter(kpi=x))
        result.append(
            {"kpi": x, "sports": sports, "evrikas": evrikas, "works": works, "books": books, 'meetings': meetings})

    return render(request, 'index.html', context={"results": result})


def all_meetings(request):
    if 'create_date' in request.POST:
        meet_date = MeetingDateModel.objects.create(date=request.POST.get('meeting_date'))
        meet_date.save()
        return redirect('/all_meetings/')
    elif 'save_meeting' in request.POST:
        n_score, meeting_id = request.POST.get('n_score'), request.POST.get('meeting_id')
        meeting_date_id, kpi_id = request.POST.get('meeting_date_id'), request.POST.get('kpi_id')
        kpi_user, meeting_date_obj = KpiModel.objects.get(id=kpi_id), MeetingDateModel.objects.get(id=meeting_date_id)
        print(meeting_id)
        print(n_score, 'score')
        if meeting_id == 'None':
            MeetingModel.objects.create(meeting_date=meeting_date_obj, score=n_score, kpi=kpi_user).save()
            return redirect('/all_meetings/')

        obj = MeetingModel.objects.get(id=meeting_id)
        obj.score = n_score
        obj.meeting_date = meeting_date_obj
        # obj.kpi = kpi_user
        obj.save()
        return redirect('/all_meetings/')

    data = []
    kpi_objects = KpiModel.objects.all()
    deadlines = list(x.date for x in MeetingDateModel.objects.all().order_by('created_at'))
    deadline_pairs = {x.date: x.id for x in MeetingDateModel.objects.all().order_by('created_at')}

    for kpi_obj in kpi_objects:
        kpi_data = {kpi_obj: []}
        work_dic = {}

        # Iterate through each WorkModel object and add to the kpi_data dictionary
        for meeting_item in kpi_obj.meeting_items.all():
            work_dic[meeting_item.meeting_date.date] = {'score': meeting_item.score, 'meeting_id': meeting_item.id,
                                                        "meeting_date_id": meeting_item.meeting_date.id}
        for i in range(len(deadlines)):
            if deadlines[i] in work_dic:
                kpi_data[kpi_obj].append({
                    'date': deadlines[i].strftime('%Y-%m-%d'),
                    'score': work_dic[deadlines[i]]['score'],
                    'meeting_id': work_dic[deadlines[i]]['meeting_id'],
                    'meeting_date_id': work_dic[deadlines[i]]['meeting_date_id']
                })
            else:
                kpi_data[kpi_obj].append({
                    'date': deadlines[i].strftime('%Y-%m-%d'),
                    'score': 0,
                    'meeting_id': None,
                    'meeting_date_id': deadline_pairs[deadlines[i]]
                })

        data.append(kpi_data)
    return render(request, 'all_meetings.html', context={'data': data, 'deadlines': deadlines})


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if User.objects.filter(email=email).exists():
            error_message = 'Email is already taken.'
            return render(request, 'signup.html', {'error_message': error_message})

        # Check if passwords match
        if pass1 != pass2:
            error_message = "Passwords don't match."
            return render(request, 'signup.html', {'error_message': error_message})

        # Create a new user account
        User.objects.create_user(username=uname, email=email, password=pass1)

        return redirect('login')  # Redirect to the login page after successful sign-up

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Username or Password is incorrect")

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect("/")


def Navbar(request):
    return render(request, 'navbar.html')


# Book
def edit_book(request, kpi_id, book_id):
    kpi = get_object_or_404(KpiModel, id=kpi_id)
    book = get_object_or_404(BookModel, id=book_id)

    if request.method == 'POST':
        n_book = request.POST.get('book')
        score = request.POST.get('score')
        bookitem = BookItem.objects.get(id=n_book)
        book.book = bookitem
        book.score = score
        book.save()

        return redirect(f'/book/{kpi_id}/')

    return render(request, 'edit_book.html', {'kpi': kpi, 'book': book})


def delete_book(request, kpi_id, book_id):
    if request.method == 'POST':
        book = get_object_or_404(BookModel, id=book_id)
        book.delete()
        return redirect(f'/book/{kpi_id}/')


def create_book(request, kpi_id):
    kpi = get_object_or_404(KpiModel, id=kpi_id)

    if request.method == 'POST':
        book_id = request.POST.get('book')
        score = request.POST.get('n_score', '')
        book = BookItem.objects.get(id=book_id)
        new_book = BookModel.objects.create(score=score, book=book, kpi=kpi)
        new_book.save()

        return redirect(f'/book/{kpi_id}/')

    return render(request, 'book.html', {'kpi': kpi})


@login_required(login_url='login')
def book(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    books = BookModel.objects.filter(kpi=kpi)
    bookitems = BookItem.objects.all()

    if request.method == 'POST':
        if 'edit_book' in request.POST:
            book_id = request.POST.get('book_id')
            return redirect('edit_book', kpi_id=id, book_id=book_id)
        elif 'delete_book' in request.POST:
            book_id = request.POST.get('book_id')
            return redirect('delete_book', kpi_id=id, book_id=book_id)
        elif 'create_book' in request.POST:
            return redirect('create_book', kpi_id=id)

    return render(request, 'book.html', {"books": books, 'kpi': kpi, 'bookitems': bookitems})


@login_required(login_url='login')
def bookItems(request):
    bookitems = BookItem.objects.all()
    if request.method == 'POST':
        title = request.POST.get("title")
        bookitem = BookItem.objects.create(title=title)
        bookitem.save()
        return redirect('/')
    return render(request, 'book_items.html', {"bookitems": bookitems})


def edit_work(request, kpi_id, work_id):
    kpi = get_object_or_404(KpiModel, id=kpi_id)
    work = get_object_or_404(WorkModel, id=work_id)

    if request.method == 'POST':
        deadline = request.POST.get('deadline')
        score = request.POST.get('score')
        description = request.POST.get('description', '')

        work.deadline = deadline
        work.score = score
        work.description = description
        work.save()

        return redirect(f'/work/{kpi_id}/')

    return render(request, 'edit_work.html', {'kpi': kpi, 'work': work})


def delete_work(request, kpi_id, work_id):
    if request.method == 'POST':
        work = get_object_or_404(WorkModel, id=work_id)
        work.delete()
        return redirect(f'/work/{kpi_id}/')


def create_work(request, kpi_id):
    kpi = get_object_or_404(KpiModel, id=kpi_id)

    if request.method == 'POST':
        deadline = request.POST.get('n_deadline')
        score = request.POST.get('n_score', '')
        description = request.POST.get('n_description', '')

        new_work = WorkModel.objects.create(deadline=deadline, score=score, description=description, kpi=kpi)
        new_work.save()

        return redirect(f'/work/{kpi_id}/')

    return render(request, 'work.html', {'kpi': kpi})


@login_required(login_url='login')
def work(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    works = WorkModel.objects.filter(kpi=kpi).order_by("deadline")

    if request.method == 'POST':
        if 'edit_work' in request.POST:
            work_id = request.POST.get('work_id')
            return redirect('edit_work', kpi_id=id, work_id=work_id)
        elif 'delete_work' in request.POST:
            work_id = request.POST.get('work_id')
            return redirect('delete_work', kpi_id=id, work_id=work_id)
        elif 'create_work' in request.POST:
            return redirect('create_work', kpi_id=id)

    return render(request, 'work.html', {"works": works, 'kpi': kpi})

@login_required(login_url='login')
def work_increase_score(request, work_id=None):
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))

    work = get_object_or_404(WorkModel, id=work_id)
    work.score += 0.5
    work.save()

    return redirect(to='all_works')

@login_required(login_url='login')
def work_increase_score(request, work_id=None):
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))

    work = get_object_or_404(WorkModel, id=work_id)
    work.score = '0.5'
    work.save()

    return redirect(to='all_works')

@login_required(login_url='login')
def work_reset_score(request, work_id=None):
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))

    work = get_object_or_404(WorkModel, id=work_id)
    work.score = '0'
    work.save()

    return redirect(to='all_works')
@login_required(login_url='login')
def work_decrease_score(request, work_id=None):
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))

    work = get_object_or_404(WorkModel, id=work_id)
    work.score = '-1'
    work.save()

    return redirect(to='all_works')

def reminder(request):
    return render(request, 'reminder.html')


@login_required(login_url='login')
def sport(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    sports = SportModel.objects.filter(kpi=kpi)

    if request.method == 'POST':
        if 'edit_sport' in request.POST:
            sport_id = request.POST.get('sport_id')
            return redirect('edit_sport', kpi_id=id, sport_id=sport_id)
        elif 'delete_book' in request.POST:
            sport_id = request.POST.get('sport_id')
            return redirect('delete_sport', kpi_id=id, sport_id=sport_id)
        elif 'create_sport' in request.POST:
            return redirect('create_sport', kpi_id=id)

    return render(request, 'sport.html', {"sports": sports, 'kpi': kpi})


def edit_sport(request, kpi_id, sport_id):
    kpi = get_object_or_404(KpiModel, id=kpi_id)
    sport = get_object_or_404(SportModel, id=sport_id)

    if request.method == 'POST':
        details = request.POST.get('details')
        score = request.POST.get('score')

        sport.details = details
        sport.score = score
        sport.save()

        return redirect(f'/sport/{kpi_id}/')

    return render(request, 'edit_sport.html', {'kpi': kpi, 'sport': sport})


def delete_sport(request, kpi_id, sport_id):
    if request.method == 'POST':
        sport = get_object_or_404(SportModel, id=sport_id)
        sport.delete()
        return redirect(f'/sport/{kpi_id}/')


def create_sport(request, kpi_id):
    kpi = get_object_or_404(KpiModel, id=kpi_id)

    if request.method == 'POST':
        details = request.POST.get('n_details')
        score = request.POST.get('n_score', '')

        new_sport = SportModel.objects.create(details=details, score=score, kpi=kpi)
        new_sport.save()

        return redirect(f'/sport/{kpi_id}/')

    return render(request, 'sport.html', {'kpi': kpi})


def edit_evrika(request, kpi_id, evrika_id):
    kpi = get_object_or_404(KpiModel, id=kpi_id)
    evrika = get_object_or_404(EvrikaModel, id=evrika_id)

    if request.method == 'POST':
        details = request.POST.get('details')
        score = request.POST.get('score', None)

        evrika.details = details
        evrika.score = score
        evrika.save()

        return redirect(f'/evrika/{kpi_id}/')

    return render(request, 'edit_evrika.html', {'kpi': kpi, 'evrika': evrika})


def delete_evrika(request, kpi_id, evrika_id):
    if request.method == 'POST':
        evrika = get_object_or_404(EvrikaModel, id=evrika_id)
        evrika.delete()
        return redirect(f'/evrika/{kpi_id}/')


def create_evrika(request, kpi_id):
    kpi = get_object_or_404(KpiModel, id=kpi_id)

    if request.method == 'POST':
        details = request.POST.get('n_details')
        score = request.POST.get('n_score', '')

        new_evrika = EvrikaModel.objects.create(details=details, score=score, kpi=kpi)
        new_evrika.save()

        return redirect(f'/evrika/{kpi_id}/')

    return render(request, 'evrika.html', {'kpi': kpi})


@login_required(login_url='login')
def evrika(request, id=None):
    kpi = get_object_or_404(KpiModel, id=id)
    evrikas = EvrikaModel.objects.filter(kpi=kpi)

    if request.method == 'POST':
        if 'edit_evrika' in request.POST:
            evrika_id = request.POST.get('evrika_id')
            return redirect('edit_evrika', kpi_id=id, evrika_id=evrika_id)
        elif 'delete_evrika' in request.POST:
            evrika_id = request.POST.get('evrika_id')
            return redirect('delete_evrika', kpi_id=id, evrika_id=evrika_id)
        elif 'create_evrika' in request.POST:
            return redirect('create_evrika', kpi_id=id)

    return render(request, 'evrika.html', {"evrikas": evrikas, 'kpi': kpi})


def all_works(request):
    if 'create_deadline' in request.POST:
        deadline = DeadlineModel.objects.create(date=request.POST.get('new_deadline'))
        deadline.save()
        return redirect('/all_works/')
    elif 'save_work' in request.POST:
        n_score, work_id = request.POST.get('n_score'), request.POST.get('work_item_id')
        deadline_id, kpi_id = request.POST.get('deadline_id'), request.POST.get('kpi_id')
        kpi_user, dead_obj = KpiModel.objects.get(id=kpi_id), DeadlineModel.objects.get(id=deadline_id)
        if work_id == 'None':
            WorkModel.objects.create(deadline=dead_obj, score=n_score, kpi=kpi_user).save()
            return redirect('/all_works/')
        obj = WorkModel.objects.get(id=work_id)
        obj.score = n_score
        obj.deadline = dead_obj
        obj.kpi = kpi_user
        obj.save()
        return redirect('/all_works/')
    data = []
    kpi_objects = KpiModel.objects.all()
    deadlines = list(x.date for x in DeadlineModel.objects.all().order_by('created_at'))
    deadline_pairs = {x.date: x.id for x in DeadlineModel.objects.all().order_by('created_at')}

    for kpi_obj in kpi_objects:
        kpi_data = {kpi_obj: []}
        work_dic = {}

        # Iterate through each WorkModel object and add to the kpi_data dictionary
        for work_item in kpi_obj.work_items.all():
            work_dic[work_item.deadline.date] = {'score': work_item.score, 'work_id': work_item.id,
                                                 "deadline_id": work_item.deadline.id}
        for i in range(len(deadlines)):
            if deadlines[i] in work_dic:
                kpi_data[kpi_obj].append({
                    'date': deadlines[i].strftime('%Y-%m-%d'),
                    'score': work_dic[deadlines[i]]['score'],
                    'work_id': work_dic[deadlines[i]]['work_id'],
                    'deadline_id': work_dic[deadlines[i]]['deadline_id']
                })
            else:
                kpi_data[kpi_obj].append({
                    'date': deadlines[i].strftime('%Y-%m-%d'),
                    'score': 0,
                    'work_id': 0,
                    'deadline_id': deadline_pairs[deadlines[i]]
                })

        data.append(kpi_data)
    return render(request, 'all_works.html', {"deadlines": deadlines, "data": data})


def all_books(request):
    if 'create_book_item' in request.POST:
        book_item = BookItem.objects.create(title=request.POST.get('new_book_item'))
        book_item.save()
        return redirect('/all_books/')
    elif 'save_book' in request.POST:
        book_score, book_id = request.POST.get('book_score'), request.POST.get('book_id')
        book_item_id, kpi_id = request.POST.get('book_item_id'), request.POST.get('kpi_id')
        kpi_user= KpiModel.objects.get(id=kpi_id)
        book_item_obj = BookItem.objects.get(id=book_item_id)
        if book_id == 'None':
            BookModel.objects.create(book=book_item_obj, score=book_score, kpi=kpi_user).save()
            return redirect('/all_books/')
        
        obj = BookModel.objects.get(id=book_id)
        obj.score = book_score
        # obj.book = dead_obj
        obj.kpi = kpi_user
        obj.save()
        return redirect('/all_books/')
    
    data = []
    kpis = KpiModel.objects.all()
    book_items = list(x.title for x in BookItem.objects.all().order_by('created_at'))
    book_pairs = {x.title: x.id for x in BookItem.objects.all().order_by('created_at')}
    for kpi_obj in kpis:
        kpi_data = {kpi_obj: []}
        book_dic = {}

        # Iterate through each BookModel object and add to the kpi_data dictionary
        for book in kpi_obj.book_items.all():
            book_dic[book.book.title] = {'score': book.score, 'book_id': book.id,
                                                "book_item_id": book.book.id}
        for i in range(len(book_items)):
                if book_items[i] in book_dic:
                    kpi_data[kpi_obj].append({
                        # 'book': book_items[i],
                        'book_id':book_dic[book_items[i]]['book_id'],
                        'score': book_dic[book_items[i]]['score'],
                        'book_item_id': book_dic[book_items[i]]['book_item_id'],
                    })
                else:
                    kpi_data[kpi_obj].append({
                        # 'book': '',
                        'book_id':None,
                        'score': 0,
                        'book_item_id': book_pairs[book_items[i]]
                    })

        data.append(kpi_data)
    return render(request, 'all_books.html', {"book_items": book_items, "data": data})
    
def all_evrikas(request):
    if 'save_evrika' in request.POST:
        score = request.POST.get('score')
        details = request.POST.get('details')
        obj = EvrikaModel.objects.get(id=request.POST.get('evrika_id'))
        obj.score = score
        obj.details = details
        obj.save()
    elif 'create_evrika' in request.POST:
        kpi_obj = KpiModel.objects.get(id=request.POST.get('kpi_id'))
        EvrikaModel.objects.create(details=request.POST.get('details'), score=request.POST.get('score'), kpi=kpi_obj).save()
        return redirect('/all_evrika/')
    evrikas = [x for x in EvrikaModel.objects.all().order_by("created_at")]
    return render(request, 'all_evrikas.html', {'data': evrikas})


def all_sports(request):
    sports = SportModel.objects.all().order_by("created_at")
    kpi_users = KpiModel.objects.all()
    if request.method == 'POST':
        if 'edit_sport' in request.POST:
            sport_id = request.POST.get('sport_id')
            kpi_sport = request.POST.get('kpi_sport')
            obj = SportModel.objects.get(id=sport_id)
            obj.details = request.POST.get('details')
            obj.score = request.POST.get('score')
            obj.save()
            return redirect('/all_sports/')

        elif 'create_sport' in request.POST:
            print(request.POST)
            kpi_user = request.POST.get('kpi_user')
            kpi = KpiModel.objects.get(id=kpi_user)
            n_score = request.POST.get('n_score')
            n_details = request.POST.get('n_details')
            obj = SportModel.objects.create(details=n_details, score=n_score, kpi=kpi)
            obj.save()
            return redirect('/all_sports/')
        
#   get method
    data = []
    kpi_objects = KpiModel.objects.all()
    sport_dates = list(x for x in SportDateModel.objects.all().order_by('created_at'))
    sport_date_pairs = {x.date: x.id for x in SportDateModel.objects.all().order_by('created_at')}
    sport_objects = SportModel.objects.all().order_by('created_at')

    for sport_date_obj in sport_dates:
        sport_data = {sport_date_obj.date: []}
        sport_dic = {}

        # Iterate through each WorkModel object and add to the kpi_data dictionary
        for sport_item in sport_date_obj.sport_date_items.all():
            sport_dic[sport_date_obj.date] = {'score': sport_item.score, 'sport_id': sport_item.id,
                                                 "sport_date_id": sport_date_obj.id, 'kpi_user':sport_item.kpi}
        
        for i in range(len(sport_dates)):
            if sport_dates[i] in sport_dic:
                sport_data[sport_date_obj.date].append({
                    'sport_date_id': sport_dates[i].id,
                    'score': sport_dic[sport_dates[i]].date['score'],
                    'sport_id': sport_dic[sport_dates[i]].date['sport_id'],
                    'kpi_user': sport_dic[sport_dates[i]].date['kpi_user']
                })
            else:
                sport_data[sport_date_obj.date].append({
                    'sport_date_id': sport_dates[i].id,
                    'score': 0,
                    'sport_id': None,
                    # 'kpi_user': deadline_pairs[deadlines[i]]
                })

        data.append(sport_data)
    print(data)
    return render(request, 'all_sports.html', {'sports': sports, 'kpi_users': kpi_users})
# [{<KpiModel: sadriddin>: [{'date': '2023-08-17', 'score': '-1', 'work_id': 1, 'deadline_id': 1}, {'date': '1221-12-21', 'score': 0, 'work_id': None, 'deadline_id': 2}]}]
# [{<KpiModel: sadriddin>: [{'date': '2023-08-17', 'score': '-1', 'work_id': 1, 'deadline_id': 1}, {'date': '1221-12-21', 'score': 0, 'work_id': None, 'deadline_id': 2}]}, {<KpiModel: user-1>: [{'date': '2023-08-17', 'score': 0, 'work_id': None, 'deadline_id': 1}, {'date': '1221-12-21', 'score': 0, 'work_id': None, 'deadline_id': 2}]}]

@login_required(login_url="login")
def edit_kpi(request, kpi_id):
    kpi = get_object_or_404(KpiModel, id=kpi_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        book_comment = request.POST.get('book_comment', None)
        upwork = request.POST.get('upwork', None)

        kpi.name = name
        kpi.book_comment = book_comment
        kpi.upwork = upwork
        kpi.save()

        return redirect(f'/kpi/')

    return render(request, 'edit_kpi.html')


@login_required(login_url="login")
def delete_kpi(request, kpi_id):
    kpi = get_object_or_404(KpiModel, id=kpi_id)
    if request.method == 'POST':
        kpi.delete()
        return redirect(f'/kpi/')


@login_required(login_url="login")
def create_kpi(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        book_comment = request.POST.get('book_comment', '')
        upwork = request.POST.get('upwork', '')

        new_kpi = KpiModel.objects.create(name=name, book_comment=book_comment, upwork=upwork)
        new_kpi.save()

        return redirect(f'/kpi/')

    return render(request, 'kpi.html')


@login_required(login_url="login")
def kpi_view(request):
    kpi_models = KpiModel.objects.all()

    if request.method == 'POST':
        if 'edit_kpi' in request.POST:
            kpi_id = request.POST.get('kpi_id')
            return redirect('edit_kpi', kpi_id=kpi_id)
        elif 'delete_kpi' in request.POST:
            kpi_id = request.POST.get('kpi_id')
            return redirect('delete_kpi', kpi_id=kpi_id)
        elif 'create_kpi' in request.POST:
            return redirect('create_kpi')
    return render(request, 'kpi.html', {"kpi_models": kpi_models})


def get_data(request):
    data = []
    kpi_objects = KpiModel.objects.all()
    deadlines = list(x.date for x in DeadlineModel.objects.all().order_by('created_at'))

    for kpi_obj in kpi_objects:
        kpi_data = {kpi_obj.name: []}
        work_dic = {}
        for x in kpi_obj.work_items.all():
            work_dic[x.deadline.date] = x.score

        # Iterate through each WorkModel object and add to the kpi_data dictionary
        for i in range(len(deadlines)):
            if deadlines[i] in work_dic:
                kpi_data[kpi_obj.name].append({deadlines[i].strftime('%Y-%m-%d'): work_dic[deadlines[i]]})
            else:
                kpi_data[kpi_obj.name].append({deadlines[i].strftime('%Y-%m-%d'): 0})
        data.append(kpi_data)
    return JsonResponse(data, safe=False)
