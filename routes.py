from flask import Blueprint,request,jsonify
from models import db,BlogPost
from datetime import datetime


blog_routes = Blueprint("blog_routes",__name__)


@blog_routes.route('/posts',methods=['POST'])
def create_post():
    data = request.get_json()
    

    if not data.get('title') or not data.get('content') or not data.get('category') or not data.get('tags'):
        return jsonify({"error": "All fields(title,content,category,tags) are required"}),400
    

    new_data = BlogPost(
        title = data['title'],
        content = data['content'],
        category = data['category'],
        tags = ",".join(data['tags'])
    )


    db.session.add(new_data)
    db.session.commit()
    
    return jsonify(new_data.to_dict()),201

@blog_routes.route('/posts/<int:blog_id>',methods=['PUT'])
def update_post(blog_id):
    data = request.get_json()

    blog_post = BlogPost.query.get(blog_id)
    if not blog_post:
        return jsonify({"error": "Blog post not found"}),404

    if not data.get('title') or not data.get('content') or not data.get('category') or not data.get('tags'):
        return jsonify({"error": "All fields(title,content,category,tags) are required"}),400
    

    blog_post.title = data['title']
    blog_post.content = data['content']
    blog_post.category = data['category']
    blog_post.tags = ",".join(data['tags'])
    blog_post.updatedAt = datetime.utcnow() # Use current timestamp

    db.session.commit()

    return jsonify(blog_post.to_dict()),200


@blog_routes.route('/posts/<int:blog_id>',methods=['DELETE'])
def delete_post(blog_id):
    data = request.get_json()

    blog_post  = BlogPost.query.get(blog_id)

    if not blog_post:
        return jsonify({"error": "Blog post not found"}),404
    
    if blog_post.id != blog_id:
        return jsonify({"error":"Forbidden"}),403
    
    db.session.delete(blog_post)
    db.session.commit()

    return '',204

@blog_routes.route('/posts/<int:blog_id>',methods=['GET'])
def get_post(blog_id):
    data = request.get_json()

    blog_post  = BlogPost.query.get(blog_id)

    if not blog_post:
        return jsonify({"error": "Blog post not found"}),404
    
    return jsonify(blog_post.to_dict()),200

@blog_routes.route('/posts', methods=['GET'])
def get_posts():
    search_term = request.args.get('term', '').lower()

    query = BlogPost.query

    if search_term:
        query = query.filter(
            BlogPost.title.ilike(f'%{search_term}%') |
            BlogPost.content.ilike(f'%{search_term}%') |
            BlogPost.category.ilike(f'%{search_term}%') |
            BlogPost.tags.ilike(f'%{search_term}%')
        )

    blog_posts = query.all()
    result = []
    for post in blog_posts:
        result.append(post.to_dict())

    return jsonify(result), 200
