use holdettedb;

create table Products (
	pid int unsigned not null unique auto_increment,
    username varchar(64) not null unique,
    image_uri tinytext not null, 
    price int unsigned not null,
    stock int unsigned not null,
    description tinytext, 
    title tinytext,
    primary key (pid)
);
create table unverified_products (
	pid int unsigned unique not null,
    primary key (pid),
    foreign key (pid) references Products(pid)
); 

create table verified_products (
	pid int unsigned unique not null,
    primary key (pid),
    foreign key (pid) references Products(pid)
);


--     TODO: Create Vendor Settings Data columns
CREATE TABLE Vendors (
	vid varchar(64) not null unique,
    primary key (vid)
);

CREATE TABLE Tags (
	tag_name varchar(32) unique not null,
    primary key (tag_name)
);

CREATE TABLE Sizes (
	size varchar(16) unique not null,
    primary key (size)
);

CREATE TABLE Vendor_Products (
	vid varchar(64) not null,
    pid int unsigned not null,
    primary key (vid),
    foreign key (vid) references Vendors(vid),
    foreign key (pid) references Products(pid)
);

CREATE TABLE Product_Tags (
	pid int unsigned not null,
	tag_name varchar(32) not null,
    primary key (pid),
    foreign key (tag_name) references Tags(tag_name),
    foreign key (pid) references Products(pid)
);

CREATE TABLE Product_Sizes(
	pid int unsigned not null,
    size varchar(16) not null,
    primary key (pid),
    foreign key (pid) references Products(pid),
    foreign key (size) references Sizes(size)
);
