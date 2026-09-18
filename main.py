from datetime import datetime
from fastapi import FastAPI,Path,Query,HTTPException,Depends
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy import DateTime, String, Float, Integer
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import func
#创建fastapi实例
app = FastAPI()

ASYNC_DATABASE_URL = "mysql+aiomysql://root:200527yp@localhost:3306/fastapi_first?charset=utf8"
async_engine = create_async_engine(ASYNC_DATABASE_URL,
                                   echo = True,
                                   pool_size = 10,
                                   max_overflow = 20)

class Base(DeclarativeBase):
    create_time : Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(),default=func.now(), comment="创建时间")
    update_time : Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now(), onupdate=func.now(), comment="更新时间")
class Book(Base):
    __tablename__ = "books"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, comment="编号")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author : Mapped[str] = mapped_column(String(255), comment="作者")
    price : Mapped[float] = mapped_column(Float, comment="价格")
    publisher : Mapped[str] = mapped_column(String(255), comment="出版社")

class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, comment="编号")
    username : Mapped[str] = mapped_column(String(255))
    password : Mapped[str] = mapped_column(String(255))

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.middleware("http")
async def middleware1(request, call_next):
    response = await call_next(request)
    return response


@app.middleware("http")
async def middleware2(request, call_next):
    response = await call_next(request)
    return response
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

async def common_parameters(skip: int = Query(0,ge=0),
                            limit: int = Query(10, le=60)):
    return {"skip": skip, "limit": limit}

@app.get("/news/news_list")
async def get_news_list(common = Depends(common_parameters)):
    return common

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

class Books(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)
    author: str = Field(min_length=2, max_length=10)
    publisher: str = Field(default="黑马出版社")
    price: float = Field(..., gt=0)

@app.post("/addBook")
async def add_book(book: Books):
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