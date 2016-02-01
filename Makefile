default:
	rm -f nba.zip
	cd src; zip -r ../nba.zip AlexaSkill.js index.js nba.js package.json node_modules/
