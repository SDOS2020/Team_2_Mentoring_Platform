const ShowMentors = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<table class="table table-hover">
			<thead style="background-color: white;">
				<tr>
					<th scope="col">#</th>
					<th scope="col">Username</th>
					<th scope="col">Actions</th>
				</tr>
			</thead>

			<tbody>
				<tr v-for="(mentor, index) in mentors" v-bind:key="mentor.id">
					<td>
						[[ index + 1 ]]
					</td>

					<td>
						<a v-bind:href="'http://127.0.0.1:8000/users/profile/' + mentor.username">
							[[ mentor.username ]]
						</a>
					</td>

					<td>
						<a class="btn btn-sm btn-primary" v-bind:href="'http://127.0.0.1:8000/mentor_mentee/my_mentor/' + mentor.username">
							Mentor-Mentee page
						</a>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
	`,
	data() {
		return {
			mentors: []
		};
	},
	created() {
		let request_url = "http://127.0.0.1:8000/api/get_mentors/";

		axios.get(request_url)
		.then(response => {
			console.log("[SUCCESS]");
			this.mentors = response.data['mentors'];
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
			this.mentors = [];
		});
	}
};
