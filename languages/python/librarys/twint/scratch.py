import twint

# Configure
config = twint.Config()
config.Search = 'squid game'
config.Lang = "en"
config.Since = '2021-09-17'
config.Until = '2021-11-26'
config.Store_json = True
config.Output = "squid game.json"

twint.run.Search(config)
