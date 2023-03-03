from flaskr import create_app
from flaskr.__init__ import scheduler
import csv

app=create_app()

from flaskr.models import Item
@scheduler.task('interval', id='do_job_1',seconds=5)
def job1():
    item = Item.load_item(0)
    data={
        "id":item.id,
        "name":item.name
    }
    
    f = open('write1.tsv', 'w')
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(data)
    f.close()
    

if __name__=="__main__":
    app.run(debug=True)
    scheduler.init_app(app)
    scheduler.start()
