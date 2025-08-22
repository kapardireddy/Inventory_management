CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,          
    product_id INT NOT NULL,        
    value NUMERIC NOT NULL,         
    transaction_id SERIAL NOT NULL, 
    created_at TIMESTAMP DEFAULT now()
);




CREATE TABLE IF NOT EXISTS totals (
    product_id INT PRIMARY KEY,
    total NUMERIC
);


ALTER TABLE public.products REPLICA IDENTITY FULL;