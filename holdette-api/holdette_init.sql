use holdettedb;


--     TODO: Create Vendor Settings Data columns
create table Vendors (
    vid varchar(64) not null unique,
    primary key (vid)
);

create table ProductStates (
    psid int unsigned not null auto_increment unique,
    state varchar(16) unique,
    primary key (psid)
);

create table Tags (
    tag_name varchar(32) unique not null,
    primary key (tag_name)
);

create table Sizes (
    size varchar(16) unique not null,
    primary key (size)
);

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
