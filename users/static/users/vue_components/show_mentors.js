const ShowMentors = {
	delimiters: ["[[", "]]"],
	components: {
		"show-mentor-mentee-stats": ShowMentorMenteeStats,
	},
	template: `
	<div>
		<table class="table table-hover">
			<thead style="background-color: white;">
				<tr>
					<th scope="col">#</th>
					<th scope="col">Username</th>
					<th scope="col">Actions</th>
					<th scope="col"></th>
					<th scope="col"></th>
				</tr>
			</thead>

			<tbody>
				<tr v-for="(mentor, index) in mentors" v-bind:key="mentor.id">
					<td>
						[[ index + 1 ]]
					</td>

					<td>
						<a v-bind:href="'/users/profile/' + mentor.username">
							[[ mentor.username ]]
						</a>
					</td>

					<td>
						<a class="btn btn-sm btn-primary" v-bind:href="'/mentor_mentee/my_mentor/' + mentor.username">
							Mentor-Mentee page
						</a>
					</td>

					<td>
						<show-mentor-mentee-stats :mentor="mentor.username" :mentee="mentee">
						</show-mentor-mentee-stats>
					</td>

					<td>
						<a
							class="btn btn-sm btn-danger"
							data-toggle="modal"
							v-bind:data-target="'#endRelModalLong' + index"
							title="End Relationship"
						>
							<i class="far fa-times-circle"></i>
						</a>
					</td>

					<!-- START MODAL - endRelModal -->
					<div class="modal fade" v-bind:id="'endRelModalLong' + index" tabindex="-1" role="dialog" v-bind:aria-labelledby="'endRelModalLongTitle' + index" aria-hidden="true">
						<div class="modal-dialog" role="document">
							<div class="modal-content">
								<div class="modal-header">
									<h5 class="modal-title" v-bind:id="'endRelModalLongTitle' + index">End Relationship</h5>
									<button type="button" class="close" data-dismiss="modal" aria-label="Close">
										<span aria-hidden="true">&times;</span>
									</button>
								</div>
								
								<div class="modal-body">
									<h5>Enter reason for ending the relationship</h5>
									<textarea v-model="end_reason" style="width: 100%;"></textarea>
								</div>
								
								<div class="modal-footer">
									<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
									<button
										v-on:click="end_relationship(mentor.username, index)"
										type="button"
										class="btn btn-danger"
									>
										Confirm
									</button>
								</div>
							</div>
						</div>
					</div>
					<!-- END MODAL -->

				</tr>
			</tbody>
		</table>
	</div>
	`,

	data() {
		return {
			mentors: [],
			end_reason: ""
		};
	},

	props: {
		mentee: {
			required: true
		}
	},

	created() {
		this.get_my_mentors();
	},

	methods: {
		get_my_mentors() {
			let request_url = "/api/get_mentors/";

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
		},

		end_relationship(username, index) {
			if (this.end_reason.length < 10) {
				alert("[INFO] Please elaborate");
				return ;
			}
			
			let request_url = "/api/end_relationship/";

			axios.get(request_url, {
				'params': {
					'username': username,
					'end_reason': this.end_reason
				}
			})
			.then(response => {
				console.log("[SUCCESS]");
				if (response.data.success) {
					this.get_my_mentors();
				}
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});

			this.end_reason = "";
			$('#endRelModal' + index).modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
		}
	}
};
