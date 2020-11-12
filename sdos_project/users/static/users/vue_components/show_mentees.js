const ShowMentees = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<table class="table table-hover">
			<thead style="background-color: white;">
				<tr>
					<th scope="col">#</th>
					<th scope="col">Username</th>
				</tr>
			</thead>

			<tbody>
				<tr v-for="(mentee, index) in mentees" v-bind:key="mentee.id">
					<td>
						[[ index + 1 ]]
					</td>

					<td>
						<a :href="'//127.0.0.1:8000/users/profile/' + mentee.username">
							[[ mentee.username ]]
						</a>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
	`,
	data() {
		return {
			mentees: []
		};
	},
	created() {
		let request_url = "http://127.0.0.1:8000/api/get_mentees/";

		axios.get(request_url)
			.then(response => {
				console.log("[SUCCESS]");
				this.mentees = response.data['mentees'];
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
				this.mentees = [];
			});
	}
};
