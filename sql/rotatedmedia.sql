DROP VIEW IF EXISTS store_RotatedMedia;
CREATE VIEW store_RotatedMedia AS
	SELECT id as media_ptr_id, name, cost_cents, price_cents, weight_oz, exterior_width, exterior_height, stock_amount,
		visible_height as vh,
		visible_width as vw,
		'Portrait' as orientation
		FROM store_Media	UNION ALL
	SELECT id as media_ptr_id, name, cost_cents, price_cents, weight_oz, exterior_width, exterior_height, stock_amount,
		store_Media.visible_width as vh,
		store_Media.visible_height + 1 as vw,
		'Landscape' as orientation
	FROM store_Media
	WHERE rotateable;

select * from store_RotatedMedia;