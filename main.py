from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse, FileResponse
#创建fastapi实例
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/hello")
async def say_hello():
    return {"msg: 你好，Fastapi"}

@app.get("/user/hello")
async def learning():
    return {"msg: 我正在学习Fastapi"}

@app.get("/books/{id}")
async def book(id: int = Path(..., gt=0, lt=101, description="书籍id在1到100间")):
    return {"id": id, "title": f"这是第{id}本书"}

@app.get("/username/{id}")
async def username(id: str):
    return {"id": id, "name": f"用户名称为{id}"}

@app.get("/author/{name}")
async def author(name: str = Path(...,max_length=10,  min_length=2, description="作者名称在2到10字符之间")):
    return {"name": name, "msg": f"作者姓名为{name}"}

@app.get("/mewss/{id}")
async def mews(id: int = Path(..., gt=0, lt=101, description="分类id在1到100之间")):
    return {"msg": f"新闻类别id为{id}"}

@app.get("/newss/{name}")
async def news(name: str = Path(..., min_length=2, max_length=10)):
    return {"msg": f"新闻类别为{name}"}

@app.get("/news/news_list")
async def get_news_list(skip: int = Query(0, lt=100, description="跳过的记录数"),
                        limit: int = Query(10, description="返回的记录数")):
    return {"skip": skip, "limit": limit}

@app.get("/book/search")
async def book_search(catgeory: str = Query("Python开发", min_length=5, max_length=255),
                      prise: int = Query(ge=50, le=100)):
    return {"catgeory": catgeory, "prise": prise}

class User(BaseModel):
    username: str = Field(default="张顺飞", min_length=2, max_length=10)
    password: str = Field(min_length=6, max_length=10)

@app.post("/regist")
async def register(user: User):
    return user

class Book(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)
    author: str = Field(min_length=2, max_length=10)
    publisher: str = Field(default="黑马出版社")
    price: float = Field(..., gt=0)

@app.post("/addBook")
async def add_book(book: Book):
    return book

@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return "<h1>Hello World</h1>"

@app.get("/file")
async def get_file():
    path = "./file/1.png"
    return FileResponse(path)

class News(BaseModel):
    id: int
    title: str
    content: str

@app.get("/news/{id}", response_model=News)
async def get_news(id: int):
    return {
        "id": id,
        "title": f"这是第{id}本书",
        "content":"飞八分钱肝肺码"
    }

@app.get("/new/{id}")
async def get_new(id: int):
    id_list = [1, 2, 3, 4, 5, 6]
    if id not in id_list:
        raise HTTPException(status_code=404, detail="查找的新闻不存在")
    return {"id": id,}