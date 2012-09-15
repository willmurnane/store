DROP VIEW IF EXISTS store_rotatedmedia;
CREATE VIEW store_rotatedmedia AS
SELECT id as media_ptr_id, name, cost_cents, price_cents, weight_oz, exterior_width, exterior_height, stock_amount, visible_height as vh, visible_width as vw, 'Portrait' as orientation FROM store_media
UNION ALL
SELECT id as media_ptr_id, name, cost_cents, price_cents, weight_oz, exterior_width, exterior_height, stock_amount,
store_media.visible_width as vh,
store_media.visible_height + 1 as vw,
'Landscape' as orientation
FROM store_media
WHERE rotateable = true;

select * from store_rotatedmedia;
