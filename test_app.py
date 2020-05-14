import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        ADMIN_TOKEN = os.getenv('ADMIN_TOKEN')
        QA_TOKEN = os.getenv('QA_TOKEN')
        PLAYER_TOKEN = os.getenv('PLAYER_TOKEN')
        database_path = os.getenv('DATABASE_URL')
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        #Set headers for the different roles testing
        self.qa_headers = { 'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + QA_TOKEN}
        self.player_headers =  { 'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + PLAYER_TOKEN}
        self.admin_headers =  { 'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + ADMIN_TOKEN}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        pass

    """
    Test all endpoints using the admin token
    """
    def test_GET_categories(self):
        res = self.client().get('/categories',
        headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])
        #Ensure each cathegory has the right attributes {"id": Int, "type": Str}
        self.assertTrue(data['categories'])
        self.assertTrue(int(data['categories'].popitem()[0]))
        self.assertEqual(type(data['categories'].popitem()[1]), str)

    def test_GET_questions(self):
        res = self.client().get('/questions',
        headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['page'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(type(data['categories']), dict)
        self.assertTrue(data['current_category'])

    def test_404_GET_questions(self):
        '''Test for a page that dont exist'''
        res = self.client().get('/questions?page=9999',
        headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    '''Assume get_questuions passed. Test pagination capabilities'''
    def test_Pagination(self):
        res = self.client().get('/questions',
        headers=self.admin_headers)
        data = json.loads(res.data)
        #print(type(data['total_questions']), type(int(data['total_questions']/QUESTIONS_PER_PAGE)))
        for page in range(int(data['total_questions']/QUESTIONS_PER_PAGE)):
            '''page starts at 0, thus adding 1'''
            res = self.client().get(f'/questions?page={page + 1}',
            headers=self.admin_headers)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

    def test_DELETE_question(self):
        '''Insert a test question to be deleted'''
        test_question = Question("question", "answer", 1, 5)
        test_question.insert()
        test_question_id = test_question.id
        res = self.client().get('/questions',
            headers=self.admin_headers)
        data = json.loads(res.data)
        # '''Get questions + our test question'''
        questions_before_delete = data["total_questions"]
        res = self.client().delete(f'/questions/{test_question_id}',
            headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        res = self.client().get('/questions',
            headers=self.admin_headers)
        data = json.loads(res.data)
        '''Ensure our test question was deleted'''
        self.assertEqual(data["total_questions"], (questions_before_delete - 1))
    
    def test_404_DELETE_question(self):
        '''Try to delete an inexistent question ID''' 
        res = self.client().delete('/questions/99999',
            headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    def test_POST_question(self):
        test_question = {"question" : "this.state.question",
        "answer": "this.state.answer",
        "difficulty": 4,
        "category": 1}
        res = self.client().post('/questions', json=test_question,
            headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_id'])
    
    def test_422_POST_question(self):
        '''If the posted question, to be created, don't have the right schema
        we abort the creation'''
        test_question = {"qqqq" : "This will fail",
        "Answer": "this.state.answer",
        "some_data": 4,
        "w00tw00t": 1}
        res = self.client().post('/questions', json=test_question,
            headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "Unprocessable Entity")
        
    
    def test_POST_search(self):
        search = {"searchTerm": "a"}
        res = self.client().post('/questions/search', json=search,
            headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_422_POST_search(self):
        '''Test for wrong search query'''
        search = {"some_query_string": "a"}
        res = self.client().post('/questions/search', json=search,
            headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_GET_questions_by_category(self):
        res = self.client().get('/categories/1/questions',
            headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['page'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_GET_questions_by_category(self):
        res = self.client().get('/categories/999999/questions',
            headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")
    
    def test_PATCH_question(self):
        test_question = {"question" : "This question was updated",
        "answer": "This is a complete new answer",
        "difficulty": 1,
        "category": 1}
        res = self.client().patch('/questions/9', json=test_question,
            headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_id'])

    def test_422_PATCH_question(self):
        test_question = {}
        res = self.client().patch('/questions/9', json=test_question,
            headers=self.admin_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    '''RBAC tests'''
#TODO add a test for quizes
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()