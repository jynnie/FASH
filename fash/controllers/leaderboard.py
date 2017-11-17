from fash import app
import fash.config as config
from fash.constants import *
from fash.utils import *

from flask import (
        render_template,
        session,
        flash,
        request,
        redirect,
        abort
    )

@app.route('/leaderboard', methods=['GET'])
@get_user()
def leaderboard():
    fampts = {'BFFL': 0, 'Funky Bobasaurs': 0, 'Pirates': 0, 'Greater than U': 0, 'Gangstas': 0}
    # try:
    engine = create_engine('sqlite:///fash.db', echo=False)
    Session = sessionmaker(bind=engine)
    db = Session()

    # CALCULATING FAMILY POINTS #
    all_com = db.query(Completed).filter(Completed.valid==True).all()
    for c in all_com: # Check all completed tasks
        u = c.user # User it belongs to
        if u != None:
            f = db.query(Users).filter(Users.id == u).first().family # Which family this belongs to
            fam = db.query(Families).filter(Families.id == f).first().name
            fampts[fam] += c.task.value
    fams = sorted(list(fampts.keys()), key=lambda x: fampts[x], reverse=True)
    # Calculating places for families #
    places = [1]
    last = fampts[fams[0]]
    for f in fams[1:]:
        if fampts[f] == last:
            places.append(places[-1])
        else:
            places.append(places[-1]+1)
            last = fampts[f]

    #     db.close()
    # except Exception as e:
    #     db.rollback()
    #     return render_template('error.html', error='Failed to retrieve completed tasks :I', user=user)

    return render_template('leaderboard.html', user=user, fams=fams, fampts=fampts, places=places)


fampts = {'BFFL': 3, 'Funky Bobasaurs': 3, 'Pirates': 3, 'Greater than U': 0, 'Gangstas': 0}
fams = ['BFFL', 'Pirates', 'Funky Bobasaurs', 'Greater than U', 'Gangstas']
places = [1]
last = fampts[fams[0]]
for f in fams[1:]:
    if fampts[f] == last:
        places.append(places[-1])
    else:
        places.append(places[-1]+1)
        last = fampts[f]
print(places)
