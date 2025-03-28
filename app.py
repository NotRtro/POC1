from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@rds-endpoint.amazonaws.com/microservices_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelos de la base de datos
class UsuarioModelo(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String)
    profile_data = Column(JSON)

class ProveedorModelo(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(String, unique=True)
    details = Column(JSON)
    status = Column(String)

class ProductoModelo(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True)
    name = Column(String)
    supplier_id = Column(String)
    lifecycle_data = Column(JSON)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Modelos Pydantic para validación
class UsuarioCrear(BaseModel):
    user_id: str
    name: str
    email: str

class ProveedorCrear(BaseModel):
    supplier_id: str
    details: dict

class ProductoCrear(BaseModel):
    product_id: str
    name: str
    supplier_id: str

# Dependencia para obtener la sesión de la base de datos
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicializando FastAPI
app = FastAPI()

# Gestión de usuarios con la base de datos
@app.post("/usuarios/")
def crear_usuario(usuario: UsuarioCrear, db: Session = Depends(obtener_db)):
    db_usuario = UsuarioModelo(
        user_id=usuario.user_id, 
        name=usuario.name, 
        email=usuario.email,
        profile_data={}
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return {"status": "Usuario creado", "user_id": db_usuario.user_id}

@app.get("/usuarios/{user_id}", response_model=UsuarioCrear)
def obtener_usuario(user_id: str, db: Session = Depends(obtener_db)):
    db_usuario = db.query(UsuarioModelo).filter(UsuarioModelo.user_id == user_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# API Endpoints para Proveedor
@app.post("/proveedores/", response_model=ProveedorCrear)
def crear_proveedor(proveedor: ProveedorCrear, db: Session = Depends(obtener_db)):
    db_proveedor = ProveedorModelo(
        supplier_id=proveedor.supplier_id, 
        details=proveedor.details,
        status="activo"
    )
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return {"status": "Proveedor registrado", "supplier_id": db_proveedor.supplier_id}

@app.get("/proveedores/{supplier_id}", response_model=ProveedorCrear)
def obtener_proveedor(supplier_id: str, db: Session = Depends(obtener_db)):
    db_proveedor = db.query(ProveedorModelo).filter(ProveedorModelo.supplier_id == supplier_id).first()
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

# API Endpoints para Producto
@app.post("/productos/", response_model=ProductoCrear)
def crear_producto(producto: ProductoCrear, db: Session = Depends(obtener_db)):
    db_producto = ProductoModelo(
        product_id=producto.product_id, 
        name=producto.name, 
        supplier_id=producto.supplier_id,
        lifecycle_data={"status": "creado"}
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return {"status": "Producto creado", "product_id": db_producto.product_id}

@app.get("/productos/{product_id}", response_model=ProductoCrear)
def obtener_producto(product_id: str, db: Session = Depends(obtener_db)):
    db_producto = db.query(ProductoModelo).filter(ProductoModelo.product_id == product_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@rds-endpoint.amazonaws.com/microservices_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelos de la base de datos
class UsuarioModelo(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String)
    profile_data = Column(JSON)

class ProveedorModelo(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(String, unique=True)
    details = Column(JSON)
    status = Column(String)

class ProductoModelo(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True)
    name = Column(String)
    supplier_id = Column(String)
    lifecycle_data = Column(JSON)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Modelos Pydantic para validación
class UsuarioCrear(BaseModel):
    user_id: str
    name: str
    email: str

class ProveedorCrear(BaseModel):
    supplier_id: str
    details: dict

class ProductoCrear(BaseModel):
    product_id: str
    name: str
    supplier_id: str

# Dependencia para obtener la sesión de la base de datos
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicializando FastAPI
app = FastAPI()

# Gestión de usuarios con la base de datos
@app.post("/usuarios/")
def crear_usuario(usuario: UsuarioCrear, db: Session = Depends(obtener_db)):
    db_usuario = UsuarioModelo(
        user_id=usuario.user_id, 
        name=usuario.name, 
        email=usuario.email,
        profile_data={}
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return {"status": "Usuario creado", "user_id": db_usuario.user_id}

@app.get("/usuarios/{user_id}", response_model=UsuarioCrear)
def obtener_usuario(user_id: str, db: Session = Depends(obtener_db)):
    db_usuario = db.query(UsuarioModelo).filter(UsuarioModelo.user_id == user_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# API Endpoints para Proveedor
@app.post("/proveedores/", response_model=ProveedorCrear)
def crear_proveedor(proveedor: ProveedorCrear, db: Session = Depends(obtener_db)):
    db_proveedor = ProveedorModelo(
        supplier_id=proveedor.supplier_id, 
        details=proveedor.details,
        status="activo"
    )
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return {"status": "Proveedor registrado", "supplier_id": db_proveedor.supplier_id}

@app.get("/proveedores/{supplier_id}", response_model=ProveedorCrear)
def obtener_proveedor(supplier_id: str, db: Session = Depends(obtener_db)):
    db_proveedor = db.query(ProveedorModelo).filter(ProveedorModelo.supplier_id == supplier_id).first()
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

# API Endpoints para Producto
@app.post("/productos/", response_model=ProductoCrear)
def crear_producto(producto: ProductoCrear, db: Session = Depends(obtener_db)):
    db_producto = ProductoModelo(
        product_id=producto.product_id, 
        name=producto.name, 
        supplier_id=producto.supplier_id,
        lifecycle_data={"status": "creado"}
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return {"status": "Producto creado", "product_id": db_producto.product_id}

@app.get("/productos/{product_id}", response_model=ProductoCrear)
def obtener_producto(product_id: str, db: Session = Depends(obtener_db)):
    db_producto = db.query(ProductoModelo).filter(ProductoModelo.product_id == product_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto
