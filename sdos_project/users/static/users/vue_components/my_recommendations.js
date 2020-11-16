const Recommendations = {
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
				<tr v-for="(recommendation, index) in recommendations" v-bind:key="recommendation.id">
					<td>
						[[ index + 1 ]]
					</td>

					<td>
						<a v-bind:href="'//127.0.0.1:8000/users/profile/' + recommendation.username">
							[[ recommendation.username ]]
						</a>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
	`,
	data() {
		return {
			recommendations: []
		}
	},
	created() {
		let request_url = "http://127.0.0.1:8000/api/get_recommendations/";

		axios.get(request_url)
		.then(response => {
			console.log("[SUCCESS]");
			this.recommendations = response.data['recommendations'];
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
			this.recommendations = [];
		});
	}
}