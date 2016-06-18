require 'sqlite3'
require 'slaw'

# Open database
db = SQLite3::Database.new "../billtracker/db.sqlite3"

# Find a few rows
query = "SELECT revisions.raw_text, bills.number
    FROM bills_billrevision AS revisions
    JOIN bills_bill as bills ON revisions.bill_id = bills.id"
generator = Slaw::ActGenerator.new
generator.parser.options = {section_number_after_title: false}

results = db.execute(query) 
text = results.first.first
bylaw = generator.generate_from_text(text)
puts bylaw.to_xml(indent: 2)