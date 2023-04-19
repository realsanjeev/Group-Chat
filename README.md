# Group-Chat
DBMS project to create a chat group web-application

# DATABASE
| user     |  	 	
|----------|		
| userid   | 		
| username | 		
| password | 		


| group      |
|------------|
| groupid(p) |
| groupname  |
| userid     |


+-------------------+          +-------------------+          +---------------------+
|       User        |          |     UserInfo      |          |    ProfilePicture    |
+-------------------+          +-------------------+          +---------------------+
| - id: int         |          | - user_id: int     |          | - id: int            |
| - username: str   | 1      * | - firstname: str   | 1      1 | - user_id: int       |
| - password: str   | ---------| - middlename: str  | ----------|                     |
|                   |          | - lastname: str    |          |                     |
+-------------------+          | - gender: str      |          |                     |
                               | - dob: str         |          |                     |
                               | - email: str       |          |                     |
                               +-------------------+          +---------------------+
                                          1 | 1
                                            |
+-------------------+          +-------------------+
|    UserGroup      |          |      Member       |
+-------------------+          +-------------------+
| - id: int         |          | - user_id: int     |
| - name: str       | 1      * | - group_id: int    |
|                   | ---------|                   |
+-------------------+          +-------------------+
                                          1 | 1
                                          |
+-------------------+          +-------------------+
|       Post        |          |        Like       |
+-------------------+          +-------------------+
| - id: int         |          | - post_id: int     |
| - content: str    | 1      * | - user_id: int     |
| - doc: date       | ---------|                   |
| - user_id: int    |          +-------------------+
| - group_id: int   |
+-------------------+

                   1 | 1
                   |
+-------------------+
|      Comment      |
+-------------------+
| - id: int         |
| - comment: str    |
| - post_id: int    |
| - user_id: int    |
| - commented_on: date |
+-------------------+

	