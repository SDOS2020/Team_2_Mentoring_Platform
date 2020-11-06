from django.http import JsonResponse
from users.models import Mentor, Mentee


# TODO: Filters
def search_users(request):
	pattern = request.GET.get('pattern')
	print(Mentor.objects.all())
	print(Mentee.objects.all())
	
	shortlist = []
	i = 0
	
	# for user in random_users:
	# 	if pattern.lower() in user['name'].lower():
	# 		shortlist.append(user)

	for user in Mentee.objects.all():
		if pattern.lower() in user.account.user.username.lower():
			shortlist.append({
				'id': i,
				'name': user.account.user.username,
				'is_mentor': False
			})
			i += 1

	for user in Mentor.objects.all():
		if pattern.lower() in user.account.user.username.lower():
			shortlist.append({
				'id': i,
				'name': user.account.user.username,
				'is_mentor': True
			})
			i += 1

	return JsonResponse(shortlist, safe=False)


users = [
	{
		'id': 1,
		'name': 'helle',
		'age': 21
	},
	{
		'id': 2,
		'name': 'kt',
		'age': 22
	},
	{
		'id': 3,
		'name': 'chillar',
		'age': 180
	},
	{
		'id': 4,
		'name': 'bagga',
		'age': 20
	},
	{
		'id': 5,
		'name': 'jelle',
		'age': 50
	}
]


random_users = [
	{
		"id": 0,
		"name": "Jillian Macias",
		"age": 24
	},
	{
		"id": 1,
		"name": "Good Delacruz",
		"age": 25
	},
	{
		"id": 2,
		"name": "Trudy Harrington",
		"age": 34
	},
	{
		"id": 3,
		"name": "Jeanette Guzman",
		"age": 23
	},
	{
		"id": 4,
		"name": "Elinor Briggs",
		"age": 25
	},
	{
		"id": 5,
		"name": "Magdalena Lyons",
		"age": 34
	},
	{
		"id": 6,
		"name": "Helene Hopper",
		"age": 29
	},
	{
		"id": 7,
		"name": "Genevieve Grant",
		"age": 26
	},
	{
		"id": 8,
		"name": "Celina Mcmahon",
		"age": 29
	},
	{
		"id": 9,
		"name": "Alexandria Hardin",
		"age": 37
	},
	{
		"id": 10,
		"name": "Estella Sampson",
		"age": 22
	},
	{
		"id": 11,
		"name": "Tate Mayer",
		"age": 25
	},
	{
		"id": 12,
		"name": "Leanne Beach",
		"age": 38
	},
	{
		"id": 13,
		"name": "Alana Gallegos",
		"age": 25
	},
	{
		"id": 14,
		"name": "Miller Riggs",
		"age": 31
	},
	{
		"id": 15,
		"name": "Rowena Padilla",
		"age": 40
	},
	{
		"id": 16,
		"name": "Forbes Buchanan",
		"age": 32
	},
	{
		"id": 17,
		"name": "Randolph Herman",
		"age": 32
	},
	{
		"id": 18,
		"name": "Cora Garcia",
		"age": 38
	},
	{
		"id": 19,
		"name": "Sherrie Kramer",
		"age": 39
	},
	{
		"id": 20,
		"name": "Tessa Jacobs",
		"age": 28
	},
	{
		"id": 21,
		"name": "Hodges Wyatt",
		"age": 28
	},
	{
		"id": 22,
		"name": "Lakisha Guy",
		"age": 20
	},
	{
		"id": 23,
		"name": "Glover Preston",
		"age": 25
	},
	{
		"id": 24,
		"name": "Margo Hudson",
		"age": 25
	},
	{
		"id": 25,
		"name": "Jennie Burns",
		"age": 20
	},
	{
		"id": 26,
		"name": "Heath Waller",
		"age": 20
	},
	{
		"id": 27,
		"name": "Lenore Wilkins",
		"age": 25
	},
	{
		"id": 28,
		"name": "Beulah Hayes",
		"age": 24
	},
	{
		"id": 29,
		"name": "Blair Lowery",
		"age": 32
	},
	{
		"id": 30,
		"name": "Arline Mendez",
		"age": 20
	},
	{
		"id": 31,
		"name": "Rhonda Golden",
		"age": 39
	},
	{
		"id": 32,
		"name": "Dolly England",
		"age": 30
	},
	{
		"id": 33,
		"name": "Willis Sims",
		"age": 37
	},
	{
		"id": 34,
		"name": "Herminia Wooten",
		"age": 31
	},
	{
		"id": 35,
		"name": "Jacqueline Maldonado",
		"age": 24
	},
	{
		"id": 36,
		"name": "Greer Benjamin",
		"age": 36
	},
	{
		"id": 37,
		"name": "Bradford Meadows",
		"age": 37
	},
	{
		"id": 38,
		"name": "Elba Potter",
		"age": 20
	},
	{
		"id": 39,
		"name": "Hardy Vasquez",
		"age": 25
	},
	{
		"id": 40,
		"name": "Taylor Cantrell",
		"age": 36
	},
	{
		"id": 41,
		"name": "Madeleine Walters",
		"age": 37
	},
	{
		"id": 42,
		"name": "Pope Gordon",
		"age": 21
	},
	{
		"id": 43,
		"name": "Strong Bird",
		"age": 26
	},
	{
		"id": 44,
		"name": "Orr Noble",
		"age": 40
	},
	{
		"id": 45,
		"name": "Margret Sellers",
		"age": 21
	},
	{
		"id": 46,
		"name": "Bates Reed",
		"age": 21
	},
	{
		"id": 47,
		"name": "Douglas Hatfield",
		"age": 22
	},
	{
		"id": 48,
		"name": "Stone Stout",
		"age": 27
	},
	{
		"id": 49,
		"name": "Mattie Oneil",
		"age": 29
	},
	{
		"id": 50,
		"name": "Tammy Jones",
		"age": 22
	},
	{
		"id": 51,
		"name": "Stanton Robbins",
		"age": 33
	},
	{
		"id": 52,
		"name": "Burnett Lester",
		"age": 36
	},
	{
		"id": 53,
		"name": "Courtney Tran",
		"age": 36
	},
	{
		"id": 54,
		"name": "Evelyn Vega",
		"age": 21
	},
	{
		"id": 55,
		"name": "Nell Castaneda",
		"age": 25
	},
	{
		"id": 56,
		"name": "Laverne Strong",
		"age": 37
	},
	{
		"id": 57,
		"name": "Teresa Mcgee",
		"age": 26
	},
	{
		"id": 58,
		"name": "Whitney Mcclain",
		"age": 23
	},
	{
		"id": 59,
		"name": "Yang Gould",
		"age": 29
	},
	{
		"id": 60,
		"name": "Darla Mccray",
		"age": 28
	},
	{
		"id": 61,
		"name": "Fannie Jefferson",
		"age": 39
	},
	{
		"id": 62,
		"name": "Gamble Dickerson",
		"age": 30
	},
	{
		"id": 63,
		"name": "Coffey Mosley",
		"age": 25
	},
	{
		"id": 64,
		"name": "Lucia Jarvis",
		"age": 28
	},
	{
		"id": 65,
		"name": "Webster Maxwell",
		"age": 36
	},
	{
		"id": 66,
		"name": "Gordon Yates",
		"age": 25
	},
	{
		"id": 67,
		"name": "Adrienne Lindsay",
		"age": 26
	},
	{
		"id": 68,
		"name": "Hilary Kirkland",
		"age": 36
	},
	{
		"id": 69,
		"name": "Felecia Clayton",
		"age": 38
	},
	{
		"id": 70,
		"name": "Mack Mcknight",
		"age": 27
	},
	{
		"id": 71,
		"name": "Susana Montoya",
		"age": 28
	},
	{
		"id": 72,
		"name": "Woods Daniel",
		"age": 21
	},
	{
		"id": 73,
		"name": "Cruz Woodard",
		"age": 35
	},
	{
		"id": 74,
		"name": "Letha Floyd",
		"age": 28
	},
	{
		"id": 75,
		"name": "Michele Bradford",
		"age": 34
	},
	{
		"id": 76,
		"name": "Cole Jacobson",
		"age": 32
	},
	{
		"id": 77,
		"name": "Lakeisha Rose",
		"age": 33
	},
	{
		"id": 78,
		"name": "Sampson Ochoa",
		"age": 30
	},
	{
		"id": 79,
		"name": "Holland Schneider",
		"age": 25
	},
	{
		"id": 80,
		"name": "Cortez Cameron",
		"age": 27
	},
	{
		"id": 81,
		"name": "Shelly Dotson",
		"age": 32
	},
	{
		"id": 82,
		"name": "Jensen Atkins",
		"age": 28
	},
	{
		"id": 83,
		"name": "Skinner Hobbs",
		"age": 37
	},
	{
		"id": 84,
		"name": "Matilda Richmond",
		"age": 38
	},
	{
		"id": 85,
		"name": "King Miranda",
		"age": 25
	},
	{
		"id": 86,
		"name": "Peters Hartman",
		"age": 32
	},
	{
		"id": 87,
		"name": "Althea Stevens",
		"age": 29
	},
	{
		"id": 88,
		"name": "Carpenter Berry",
		"age": 20
	},
	{
		"id": 89,
		"name": "Brittney Warren",
		"age": 38
	},
	{
		"id": 90,
		"name": "Humphrey Maddox",
		"age": 25
	},
	{
		"id": 91,
		"name": "Deanne Mckinney",
		"age": 21
	},
	{
		"id": 92,
		"name": "Terrie Estes",
		"age": 30
	},
	{
		"id": 93,
		"name": "Irma Michael",
		"age": 40
	},
	{
		"id": 94,
		"name": "John Duffy",
		"age": 34
	},
	{
		"id": 95,
		"name": "Alyson Turner",
		"age": 36
	},
	{
		"id": 96,
		"name": "Mamie Simpson",
		"age": 39
	},
	{
		"id": 97,
		"name": "Contreras Watkins",
		"age": 30
	},
	{
		"id": 98,
		"name": "Chandler Rivers",
		"age": 34
	},
	{
		"id": 99,
		"name": "Briggs Kim",
		"age": 23
	}
]
