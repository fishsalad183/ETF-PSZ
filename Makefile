test_scrapy_shell_vozilo_list:
	scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0' 'https://www.polovniautomobili.com/auto-oglasi/pretraga?page=1&sort=basic&city_distance=0&showOldNew=all&without_price=1'

test_scrapy_shell_vozilo_page:
	scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0' 'https://www.polovniautomobili.com/auto-oglasi/19775118/alfa-romeo-147-16-ts-distinctive?attp=p1_pv0_pc1_pl1_plv0'

test_scrapy_shell_nekretnina_list:
	scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0' 'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/lista/po-stranici/10/'

test_scrapy_shell_nekretnina_page:
	scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0' 'https://www.nekretnine.rs/stambeni-objekti/stanovi/kompletno-renoviran-dvoiposoban-stan-na-novom-naselju/NkHFDDZyOx4/'

