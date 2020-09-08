from sqlalchemy.orm import Session
from sqlalchemy import and_

import graphicone_models as models
import graphicone_social_relations as social


def calc_percent_pros_and_cons(pros, cons):
    if pros + cons == 0:
        pros = 50
    elif pros + cons == -2:
        return pros, cons
    else:
        pros = round(pros / (pros + cons) * 100)

    cons = 100 - pros

    return pros, cons


def get_pros_and_cons_for_graph(graph_record):

    count_pros = count_cons = sentiment_count_pros = sentiment_count_cons = \
        fundamental_count_pros = fundamental_count_cons = -1

    if graph_record.pros_and_cons:

        if graph_record.graph_type == 'IPO':
            sentiment_count_pros = sentiment_count_cons = fundamental_count_pros = fundamental_count_cons = 0
        else:
            count_pros = count_cons = 0

        for p_c in graph_record.pros_and_cons:
            if p_c.pros_and_cons_votes:

                for vote in p_c.pros_and_cons_votes:
                    if graph_record.graph_type == 'IPO':
                        if p_c.category:
                            if p_c.category[0].category == 'Fundamental view':
                                if vote.value:
                                    fundamental_count_pros += 1
                                else:
                                    fundamental_count_cons += 1
                            elif p_c.category[0].category == 'Sentiment analysis':
                                if vote.value:
                                    sentiment_count_pros += 1
                                else:
                                    sentiment_count_cons += 1
                    if vote.value:
                        count_pros += 1
                    else:
                        count_cons += 1

        if graph_record.graph_type != 'FOW':
            sentiment_count_pros, sentiment_count_cons = calc_percent_pros_and_cons(
                sentiment_count_pros, sentiment_count_cons
            )

            fundamental_count_pros, fundamental_count_cons = calc_percent_pros_and_cons(
                fundamental_count_pros, fundamental_count_cons
            )

            count_pros, count_cons = calc_percent_pros_and_cons(count_pros, count_cons)

    return count_pros, count_cons, sentiment_count_pros, sentiment_count_cons, fundamental_count_pros, \
        fundamental_count_cons


def get_full_graphs_objects_from_graphs_records(db, graph_records, username):
    graphs_answer = list()

    for graph_record in graph_records:
        count_pros, count_cons, sentiment_count_pros, sentiment_count_cons, fundamental_count_pros, \
            fundamental_count_cons = get_pros_and_cons_for_graph(graph_record)

        graph = dict(
            article_link=graph_record.article_link,
            count_cons=count_cons,
            count_pros=count_pros,
            sentiment_count_cons=sentiment_count_cons,
            sentiment_count_pros=sentiment_count_pros,
            fundamental_count_cons=fundamental_count_cons,
            fundamental_count_pros=fundamental_count_pros,
            description=graph_record.description,
            equities=[
                dict(ticker=equity.equity_id, name=equity.equity_data.name)
                for equity in graph_record.equities if equity.equity_data
            ],
            id=graph_record.id,
            name=graph_record.name,
            owner=graph_record.owner,
            publish_date=graph_record.publish_date,
            source=graph_record.source,
            tags=[dict(id=tag_record.graph_id, name=tag_record.value) for tag_record in graph_record.tags],
            image_url=list(
                map(lambda s, m, l: dict(small=s, medium=m, large=l),
                    graph_record.link_small, graph_record.link_medium, graph_record.link_large)
            )
        )
        graph['owner']['user_status'] = social.get_user_status(db, username,
                                                               requested_username=graph['owner']['username'])

        graphs_answer.append(graph)

    return graphs_answer


def get_users_feed_graphs(db: Session, feed_owner: str, custom_limit: int, username: str):

    graph_records = db.query(models.Graph).filter(
        and_(models.Graph.location == 'feed', models.Graph.location_id == feed_owner)
    ).order_by(models.Graph.publish_date.desc()).limit(custom_limit)

    return get_full_graphs_objects_from_graphs_records(db, graph_records, username)


def get_boards_graphs(db: Session, board_id: str, username: str):

    graph_records = db.query(models.Graph).filter(
        and_(models.Graph.location == 'board', models.Graph.location_id == board_id)
    ).order_by(models.Graph.publish_date.desc()).all()

    return get_full_graphs_objects_from_graphs_records(db, graph_records, username)
