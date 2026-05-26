USE ecommerce_project;

SELECT *
FROM orders;

-- Profitability by payment method
SELECT 
    PaymentMethod,
    SUM(TotalPrice) AS revenue,
    COUNT(*) AS orders,
    SUM(CASE WHEN OrderStatus = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(1.0 * SUM(CASE WHEN OrderStatus = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate,
    ROUND(SUM(TotalPrice) / COUNT(*), 2) AS avg_order_value
FROM Orders
GROUP BY PaymentMethod
ORDER BY revenue DESC;

-- Profitability by marketing channels
SELECT 
    ReferralSource,
    SUM(TotalPrice) AS revenue,
    COUNT(*) AS orders,
    ROUND(SUM(TotalPrice) / COUNT(*), 2) AS avg_order_value
FROM Orders
GROUP BY ReferralSource
ORDER BY revenue DESC;

-- Profitability by coupons
SELECT 
    CASE 
        WHEN CouponCode IS NULL OR TRIM(CouponCode) = '' THEN 'No Coupon'
        ELSE 'Coupon Used'
    END AS coupon_status,
    SUM(TotalPrice) AS revenue,
    COUNT(*) AS orders,
    ROUND(1.0 * SUM(CASE WHEN OrderStatus = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate
FROM Orders
GROUP BY coupon_status;