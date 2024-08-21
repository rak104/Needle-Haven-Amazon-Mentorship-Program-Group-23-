DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS Store; 
DROP TABLE IF EXISTS Product; 
DROP TABLE IF EXISTS ProductImages;    
DROP TABLE IF EXISTS CHATT;    
DROP TABLE IF EXISTS CHATTMESSAGES;
DROP TABLE IF EXISTS RECOMMENDATIONS;  
DROP TABLE IF EXISTS MODELS; 

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Store hashed password
    email VARCHAR(50) NOT NULL,
    first_name VARCHAR(50),               
    last_name VARCHAR(50),                 
    date_of_birth DATE,                  
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    last_login TIMESTAMP ,                 
    is_active BOOLEAN DEFAULT TRUE        
);     

CREATE TABLE Store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    address VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Store hashed password
    phone_number VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL, -- Increased length for better descriptions
    rating INTEGER CHECK (rating >= 0 AND rating <= 5), -- Rating constraint
    logo_path VARCHAR(255) 
);   

CREATE TABLE Product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(50)  NOT NULL,
    subcategory VARCHAR(50)  NOT NULL,
    type  VARCHAR(50)  NOT NULL,
    store VARCHAR(50) NOT NULL,
    color VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL, -- Increased length for better descriptions
    price INTEGER NOT NULL CHECK (price >= 0), -- Price constraint
    rating INTEGER CHECK (rating >= 0 AND rating <= 5), -- Rating constraint
    store_id INTEGER NOT NULL,
    date_of_release DATE NOT NULL,
    image_path VARCHAR(255) NOT NULL, 
    image_path_2 VARCHAR(255) ,
    image_path_3 VARCHAR(255) , 
    image_path_4 VARCHAR(255) , 
    image_path_5 VARCHAR(255) ,  
    size VARCHAR(255) NOT NULL,
    FOREIGN KEY (store_id) REFERENCES Store(id)
);  

CREATE TABLE CHATT (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (store_id) REFERENCES Store(id)
);    

CREATE TABLE CHATTMESSAGES (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    message VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES CHATT(id)
);

CREATE TABLE RECOMMENDATIONS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);  

CREATE TABLE MODELS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT NOT NULL,   
    model_path VARCHAR(255) NOT NULL
);

-- Create Orders table
CREATE TABLE Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,  -- Reference to the user placing the order
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp for when the order is placed
    total_price DECIMAL(10, 2) NOT NULL CHECK (total_price >= 0),  -- Total price of the order
    status VARCHAR(50) DEFAULT 'Pending', -- Order status (e.g., Pending, Shipped, Delivered, Cancelled)
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Create OrderItems table
CREATE TABLE OrderItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,  -- Reference to the order
    product_id INTEGER NOT NULL, -- Reference to the product
    quantity INTEGER NOT NULL CHECK (quantity > 0),  -- Quantity of the product
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),  -- Price of the product at the time of purchase
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);
