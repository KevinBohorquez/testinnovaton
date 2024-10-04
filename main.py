from fasthtml.common import *

db = database('data/auther.db')

css = Style('''
    :root {
        --pico-font-size: 100%;
        --pico-font-family: "Arial, sans-serif";
        background-color: #f0f0f0;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    Body {
        min-height: 100vh;
        background: url(static/background.jpg)
    }
    
    .header-text{
        font-family: 'Times New Roman', Times, serif; 
        color: white;
        font-size: 1.2rem;
    }
    
    .header {   
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        padding: 1.3rem 10%;
        display: flex;
        justify-content:space-between;
        align-items: center;
        z-index: 100;
        background: rgb(0, 0, 0, 0.4);
    }
    
    .header::after{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,.4), transparent);
        transition: .5s;
    }
    
    .header:hover::after{
        left:100%;
    }
    
    .navbar a {
        left: 0;
        position: relative;
        font-size: 1.15rem;
        color: white;
        font.weight: 500;
        text-decoration: none;
        margin-left: 40px;
        opacity: 1;
    }
    
    .navbar a::before {
        content: '';
        top: -4px;
        left: -4px;
        position: absolute;
        width: 110%;
        height: 2px;
        background: white;
        opacity: 0.7;
        z-index: 1;
    }
    
    #check {
        display: none;
    }
    
    .icons{
        position: absolute;
        right: 5%;
        font-size: 2.8rem;
        color: #fff;
        cursor: pointer;
        display: none !important;
    }
    
    /*Breakpoint :v*/
    
    @media (max-width: 767px){
        .icons{
            display: block !important;
        }
        
        #check:checked~.icons #menu-icon {
            display: none;
        }
        
        .icons #close-icon{
            display: none;
        }
        
        #check:checked~.icons #close-icon {
            display: block;
        }
        
        .navbar{
            position: absolute;
            top: 100%;
            left: 0;
            width: 100%;
            height: 0;
            background: rgb(0, 0, 0, 0.2);
            background-filter: blur(50px);
            overflow: hidden;
            transition: .3s ease;
        }
        
        #check:checked~.navbar {
            height: 11.5rem;
        }
        
        .navbar a {
            display: block;
            font-size: 1.1rem;
            margin: 1.5rem;
            text-align: center;
            transform: translateY(-50px);
            opacity: 0;
            transition: .3s ease;
        }
        
        #check:checked~.navbar a {
            transform: translateY(0);
            opacity: 1;
            transition-delay: calc(.15s * var(--i));
        }
        
        .navbar a::before {
            top: -4px;
            text-align: center;
            position: relative;
            height: 2px;
            opacity: 0.7;
            z-index: 1;
            width: 10rem;
        }
    }
    ''')

class User:
    username: str
    pwd: str


class Book:
    id: int
    title: str
    auther: str
    price: int
    pages: int
    published: bool
    published_date: str


users = db.create(User, pk='username')
books = db.create(Book)


def lookup_user(u, p):
    try:
        user = users[u]
    except NotFoundError:
        user = users.insert(username=u, pwd=p)
    return user.pwd == p


auth_middleware = user_pwd_auth(
    lookup_user)

app = FastHTML(middleware=[auth_middleware],
            hdrs=(picolink,
                    css))

rt = app.route

id_curr = 'current-book'
def mk_input(**kw): return Input(**kw)
def clr_details(): return Div(hx_swap_oob='innerHTML', id=id_curr)
def tid(id): return f'book-{id}'

PER_PAGE = 10

@rt("/")
async def get(request, auth):

    page = int(request.query_params.get('page', 1))

    total_books = len(books())

    total_pages = (total_books + PER_PAGE - 1) // PER_PAGE

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    paginated_books = books()[start:end]

    search_bar = Input(
        id="q",
        placeholder="Buscar por titulo o autor...",
        hx_get="/filter_books",
        target_id='book-rows')

    published_filter = CheckboxX(
        id="published_filter",
        label='Solo libros publicados',
        hx_get="/filter_books",
        target_id='book-rows',
        style="margin-bottom: 10px;"
    )

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    pagination = Div(
        A("Previous", href=f"/?page={prev_page}",
        style="margin-right: 10px;") if prev_page else '',
        A("Next", href=f"/?page={next_page}") if next_page else '',
        style="margin-top: 10px; text-align: center;"
    )

    add = Div(
        H4("Añadir Libro"),
        Form(Group(
            mk_input(placeholder="Titulo", name="title",
                    id="title", required=True),
            mk_input(placeholder="Autor", name="auther", id="auther"),
            mk_input(placeholder="Precio", type="number",
                    name="price", id="price"),
            mk_input(placeholder=" Numero de Paginas", type="number",
                    name="pages", id="pages"),
            mk_input(placeholder="Fecha de Publicacion", type="date",
                    name="published_date", id="published_date"),
            Button("Añadir")),
            CheckboxX(id="published", name="published", label='Publicado'),
            hx_post="/", target_id='book-rows', hx_swap="beforeend"

        )
    )

    card = Card(H4(f"Libros ({total_books} libros en total)"),
                search_bar,
                published_filter,
                Table(
                    Thead(Tr(Th("Titulo"), Th("Autor"), Th("Precio"), Th("Paginas"), Th(
                        "Publicado"), Th("Fecha de Publicacion"), Th("Editar"))),
                    Tbody(*[book.__ft__()
                        for book in paginated_books], id='book-rows')
    ),
        header=add,
        footer=Div(pagination,
                Div(id=id_curr)  
                )
    )

    top = Grid(Div(A('logout', href=basic_logout(request)),
            style='text-align: right'))

    return (
            Head(
                Title("Página con FastHTML"),
                Link(rel='stylesheet', href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css')
            ),
            Body(
                Header(
                    Span(f"Book Management (Page {page})", _class="header-text"),
                    Input(type="checkbox", id="check"),
                    Label(
                        I(_class="bx bx-menu", id="menu-icon"),
                        I(_class="bx bx-x", id="close-icon"),
                        _class="icons", _for="check"
                    ),
                    Div(
                        A("FisiBiblioteca", href="#", style="--i:0"),
                        A("Home", href="#", style="--i:1"),
                        A("Sobre nosotros", href="#", style="--i:2"),
                        _class = "navbar"),
                    _class = "header"
                ),P("."),P("."),
                Titled(top, card)
            ),
        )


@patch
def __ft__(self: Book):
    show = AX(self.title, f'/books/{self.id}', id_curr)
    edit = AX('edit', f'/edit/{self.id}', id_curr)
    dt = '✅ ' if self.title else ''
    return Tr(
        Td(dt, show), Td(self.auther), Td(self.price), Td(self.pages),
        Td(self.published), Td(self.published_date), Td(edit),
        id=tid(self.id)
    )


@rt("/filter_books")
async def filter_books(request):
    q = request.query_params.get('q', None)
    published_filter = request.query_params.get('published_filter', None)
    page = int(request.query_params.get('page', 1))
    filtered_books = books()

    if q:
        filtered_books = [book for book in books() if q.lower(
        ) in book.title.lower() or q.lower() in book.auther.lower()]

    if published_filter:
        filtered_books = [book for book in filtered_books if book.published]


    total_books = len(filtered_books)
    total_pages = (total_books + PER_PAGE - 1) // PER_PAGE

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    paginated_books = filtered_books[start:end]

    if not paginated_books:
        return Tr(Td(
            "No books found", colspan=6,
            style="text-align: center; color: red;"))

    return Tr(
        *[book.__ft__() for book in paginated_books],
        id='book-rows'
    )


@rt("/books/{id}")
async def delete(id: int):
    """Delete a book"""
    books.delete(id)
    return clr_details()


@rt("/")
async def post(book: Book):
    return books.insert(book), mk_input(hx_swap_oob='true')


@rt("/edit/{id}")
async def get(id: int):
    res = Div(
        H4("Edit Book"),
        Form(Group(Input(id="title"),
                Input(id="auther"),
                Input(id="price", type="number"),
                Input(id="pages", type="number"),
                Input(id="published_date", type="date"),
                Button("Save")),
            Hidden(id="id"), CheckboxX(id="published", label='Published'),
            hx_put="/", target_id=tid(id), id="edit")
    )
    return fill_form(res, books[id])


@rt("/")
async def put(book: Book):
    return books.upsert(book), clr_details()


@rt("/books/{id}")
async def get(id: int):
    book = books[id]
    btn = Button('Delete Book', hx_delete=f'/books/{book.id}',
                target_id=tid(book.id), hx_swap="outerHTML")
    btn.style = 'background-color: red; border: none;'
    return Div(H2(f"Book Title: {book.title}"),
            H6(f"Published: {"Yes" if book.published else "No"}"),
            btn)

serve()