from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, VARCHAR, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.mysql import TINYTEXT, INTEGER


Base = delcarative_base()

class Vendor(Base):
	__tablename__ = 'vendor'
	vid = Column('vid', VARCAR(64), primary_key=True)

class ProductState(Base):
	__tablename__ = 'ProductState'
	psid = Column('psid', Integer, primary_key=True)
	state = Column('state', VARCHAR(16))

class Tag(Base):
	__tablename__ = 'Tag'
	tag_name = Column('name', VARCHAR(32), primary_key=True)

class Size(Base):
	size = Column('size', VARCHAR(16), primary_key=True)

class Product(Base):
	pid = Column('pid', Integer, primary_key=True)
	username = Column('username', VARCHAR(64), nullable=False, unique=True)
	uri = Column('uri', TINYTEXT, nullable=False)
	price = Column('price', INTEGER(unsigned=True), nullable=False)
	stock = Column('stock', INTEGER(unsigned=True), nullable=False)
	description = Column('description', TINYTEXT)
	title = Column('title', TINYTEXT)
	state = Column('state', INTEGER(unsigned=True), nullable=False, default=0)
	relationship('')


use holdettedb;


--     TODO: Create Vendor Settings Data columns

create table Products (
    pid int unsigned not null unique auto_increment,
    username varchar(64) not null unique,
    image_url tinytext not null, 
    price int unsigned not null,
    stock int unsigned not null,
    description tinytext, 
    title tinytext,
    state int unsigned not null default 0,
    constraint Products_state_constraint
        foreign key (state) references States(psid),
    primary key (pid)
);

create table VendorProducts (
    vid varchar(64) not null,
    pid int unsigned not null,
    primary key (vid),
    constraint VendorProducts_vid_constraint
        foreign key (vid) references Vendors(vid),
    constraint VendorProducts_pid_constraint
        foreign key (pid) references Products(pid)
);

create table ProductTags (
    pid int unsigned not null,
    tag_name varchar(32) not null,
    primary key (pid),
    constraint ProductTags_tag_name_constraint
        foreign key (tag_name) references Tags(tag_name),
    constraint ProductTags_pid_constraint
        foreign key (pid) references Products(pid)
);

create table ProductSizes(
    pid int unsigned not null,
    size varchar(16) not null,
    primary key (pid),
    constraint ProductSizes_pid_constraint
        foreign key (pid) references Products(pid),
    constraint ProductSizes_size_constraint
        foreign key (size) references Sizes(size)
);
