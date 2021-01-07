const AddResearchExperience = {
	delimiters: ["[[", "]]"],
	template: `
		<div>
			Research Experience
			<a
				class="btn btn-sm btn-primary"
				data-toggle="modal"
				data-target="#addReModalLong"
				style="float: right;"
			>
				Add More
			</a>

			<!-- START MODAL - addReModal -->
			<div class="modal fade" id="addReModalLong" tabindex="-1" role="dialog" aria-labelledby="addReModalLongTitle" aria-hidden="true">
				<div class="modal-dialog" role="document">
					<div class="modal-content">
						<div class="modal-header">
							<h5 class="modal-title" id="addReModalLongTitle">Add Education</h5>
							<button type="button" class="close" data-dismiss="modal" aria-label="Close">
								<span aria-hidden="true">&times;</span>
							</button>
						</div>

						<div class="modal-body">
							<h5>Position</h5>
							<input v-model="position" style="width: 100%;">
							</div>
							
							<div class="modal-body">
							<h5>Start Date</h5>
							<input v-model="start_date" type="date" required>
							</div>
							
						<div class="modal-body">
						<h5>End Date</h5>
							<input v-model="end_date" type="date" required>
							</div>
							
							<div class="modal-body">
							<h5>Organization</h5>
							<input v-model="organization" style="width: 100%;">
						</div>

						<div class="modal-body">
							<h5>Detail</h5>
							<textarea v-model="detail" style="width: 100%;"></textarea>
						</div>


						
						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
							<button
								v-on:click="add_research_experience()"
								type="button"
								class="btn btn-success"
							>
								Add
							</button>
						</div>
					</div>
				</div>
			</div>
			<!-- END MODAL -->

			<table class="table table-hover table-light table-sm">
				<tr v-for="(_, i) in positions.length" :key="i">
					<td>
						<b> [[ positions[i] ]] </b>
						<br/>
						<i> [[ start_dates[i] ]] - [[ end_dates[i] ]] </i>
						<br/>
						<b> [[ organizations[i] ]] </b>
						<br/>
						[[ details[i] ]]
						<hr>
					</td>
				</tr>
			</table>
		</div>
	`,

	data () {
		return {
			positions: [],
			start_dates: [],
			end_dates: [],
			organizations: [],
			details: [],
			
			position: '',
			start_date: '',
			end_date: '',
			organization: '',
			detail: '',
		}
	},
	created () {
		this.get_research_experience();
	},
	methods : {
		get_research_experience() {
			let request_url = "http://127.0.0.1:8000/api/get_research_experience/";

			axios.get(request_url)
			.then(response => {
				console.log("[SUCCESS]");
				this.positions = response.data['positions'];
				this.start_dates = response.data['start_dates'];
				this.end_dates = response.data['end_dates'];
				this.organizations = response.data['organizations'];
				this.details = response.data['details'];
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
				this.positions = [];
				this.start_dates = [];
				this.end_dates = [];
				this.organizations = [];
				this.details = [];
			});
		},

		add_research_experience() {
			let request_url = "http://127.0.0.1:8000/api/add_research_experience/";

			axios.get(request_url, {
				'params' : {
					'position': this.position,
					'start_date': this.start_date,
					'end_date': this.end_date,
					'organization': this.organization,
					'detail': this.detail,
				}
			})
			.then(response => {
				console.log("[SUCCESS]");
				this.get_research_experience();
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
			
			$('#addReModalLong').modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
			
			this.position = '';
			this.start_date = '';
			this.end_date = '';
			this.organization = '';
			this.detail = '';
		},
	}
}