const ShowMentees = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<table class="table table-hover">
			<thead style="background-color: white;">
				<tr>
					<th scope="col">#</th>
					<th scope="col">Username</th>
					<th scope="col">Actions</th>
					<th scope="col"></th>
				</tr>
			</thead>

			<tbody>
				<tr v-for="(mentee, index) in mentees" v-bind:key="mentee.id">
					<td>
						[[ index + 1 ]]
					</td>

					<td>
						<a v-bind:href="'/users/profile/' + mentee.username">
							[[ mentee.username ]]
						</a>
					</td>

					<td>
						<a class="btn btn-sm btn-primary" v-bind:href="'/mentor_mentee/my_mentee/' + mentee.username">
							Mentor-Mentee page
						</a>
					</td>

					<td>
						<a
							class="btn btn-sm btn-danger"
							data-toggle="modal"
							v-bind:data-target="'#endRelModalLong' + index"
						>
							End relationship
						</a>
					</td>

					<!-- START MODAL - endRelModal -->
					<div class="modal fade" v-bind:id="'endRelModalLong' + index" tabindex="-1" role="dialog" v-bind:aria-labelledby="'endRelModalLongTitle' + index" aria-hidden="true">
						<div class="modal-dialog" role="document">
							<div class="modal-content">
								<div class="modal-header">
									<h5 class="modal-title" v-bind:id="'endRelModalLongTitle' + index">Modal title</h5>
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
										v-on:click="end_relationship(mentee.username, index)"
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
			mentees: [],
			end_reason: ""
		};
	},
	created() {
		this.get_my_mentees();
	},

	methods: {
		get_my_mentees() {
			let request_url = "/api/get_mentees/";
	
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
		},

		end_relationship(username, index) {
			if (this.end_reason.length < 10) {
				alert("[INFO] Please elaborate");
				return;
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
					this.get_my_mentees();
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
