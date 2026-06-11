USE ecommerce_project;

SELECT *
FROM orders;

-- Profitability by payment method & coupon usage
SELECT
    CASE
        WHEN CouponCode IS NULL OR TRIM(CouponCode) = ''
        THEN 'No Coupon'
        ELSE 'Coupon Used'
    END AS coupon_status,
    PaymentMethod,
    ROUND(SUM(TotalPrice), 2) AS revenue,
    COUNT(*) AS orders,
    SUM(CASE WHEN OrderStatus = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(1.0 * SUM(CASE WHEN OrderStatus = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate,
    ROUND(100.0 * SUM(TotalPrice)/ SUM(SUM(TotalPrice)) OVER (PARTITION BY PaymentMethod), 2) AS coupon_revenue_share
FROM Orders
GROUP BY PaymentMethod, coupon_status;

-- Profitability by marketing channels & coupon usage
SELECT 
    CASE
        WHEN CouponCode IS NULL OR TRIM(CouponCode) = ''
        THEN 'No Coupon'
        ELSE 'Coupon Used'
    END AS coupon_status,
    ReferralSource,
    ROUND(SUM(TotalPrice), 2) AS revenue,
    COUNT(*) AS orders,
    SUM(CASE WHEN OrderStatus = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(1.0 * SUM(CASE WHEN OrderStatus = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate,
    ROUND(100.0 * SUM(TotalPrice)/ SUM(SUM(TotalPrice)) OVER (PARTITION BY ReferralSource), 2) AS coupon_revenue_share
FROM Orders
GROUP BY ReferralSource, coupon_status;
