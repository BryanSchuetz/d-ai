# Setup Langchain Integration
from dotenv import load_dotenv
load_dotenv()

from langchain.llms import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document
import requests
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate

# Gather Sources
def get_dai_data(page):
  url = f"{page}"
  data = requests.get(url).json()
  return Document(
      page_content=(data["content"]),
      metadata={"source": f"{page}"}
  )

sources = [
  get_dai_data("https://dai-global-developments.com/post-api/the-re-greening-of-iraq-restoring-marshlands.json"),
  get_dai_data("https://dai-global-developments.com/post-api/market-driven-approach-delivers-far-reaching-results-in-burundi.json"),
  get_dai_data("https://dai-global-developments.com/post-api/project-brings-together-divergent-ethnic-groups-in-sri-lanka.json"),
  get_dai_data("https://dai-global-developments.com/post-api/haitian-farmers-see-increased-income-while-better-managing-their-natural-resources.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-niger-delta-chevron-launches-new-paradigm-for-corporate-social-investment.json"),
  get_dai_data("https://dai-global-developments.com/post-api/science-into-action-turning-climate-studies-into-decision-making-tools.json"),
  get_dai_data("https://dai-global-developments.com/post-api/amplifying-the-voice-of-business-to-drive-policy-reform-in-a-difficult-environment.json"),
  get_dai_data("https://dai-global-developments.com/post-api/rethinking-participatory-development-from-critique-to-better-practice.json"),
  get_dai_data("https://dai-global-developments.com/post-api/doing-more-with-doing-business-vietnam-provincial-competitiveness-index.json"),
  get_dai_data("https://dai-global-developments.com/post-api/project-helps-vietnam-cut-red-tape-hone-competitiveness-and-boost-economic-growth.json"),
  get_dai_data("https://dai-global-developments.com/post-api/project-improves-business-environment-in-morocco-in-midst-of-political-upheaval.json"),
  get_dai_data("https://dai-global-developments.com/post-api/competitiveness-initiative-simplifies-business-in-vietnam.json"),
  get_dai_data("https://dai-global-developments.com/post-api/dai-security-chief-discusses-importance-of-local-security-and-training.json"),
  get_dai_data("https://dai-global-developments.com/post-api/helping-a-south-african-mining-giant-invest-for-results-in-its-local-communities.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-arid-jordan-idara-motivated-citizens-government-to-conserve-precious-water.json"),
  get_dai_data("https://dai-global-developments.com/post-api/the-case-for-supplier-development.json"),
  get_dai_data("https://dai-global-developments.com/post-api/thousands-worldwide-find-environmental-solutions-at-frameweb.json"),
  get_dai_data("https://dai-global-developments.com/post-api/usaid-star-project-helped-propel-vietnam-into-the-global-economy.json"),
  get_dai_data("https://dai-global-developments.com/post-api/youth-music-and-popular-voice-in-the-democratic-republic-of-the-congo.json"),
  get_dai_data("https://dai-global-developments.com/post-api/a-cash-lite-world-safe-cheap-and-convenient-payments-for-all.json"),
    get_dai_data("https://dai-global-developments.com/post-api/a-new-financial-model-putting-the-individual-at-the-centre.json"),
  get_dai_data("https://dai-global-developments.com/post-api/are-the-pacific-islands-ripe-for-mobile-money.json"),
  get_dai_data("https://dai-global-developments.com/post-api/benefits-of-bringing-mobile-banking-to-the-unbanked.json"),
  get_dai_data("https://dai-global-developments.com/post-api/beyond-financial-inclusion.json"),
  get_dai_data("https://dai-global-developments.com/post-api/business-booms-for-farmers-who-solved-supply-problem-for-top-regional-business.json"),
  get_dai_data("https://dai-global-developments.com/post-api/development-insights-on-the-frontlines-of-asymmetric-warfare.json"),
  get_dai_data("https://dai-global-developments.com/post-api/does-microfinance-work.json"),
  get_dai_data("https://dai-global-developments.com/post-api/financial-education-time-for-a-re-think.json"),
  get_dai_data("https://dai-global-developments.com/post-api/financial-inclusion-a-wealth-of-perspectives.json"),
  get_dai_data("https://dai-global-developments.com/post-api/great-expectations.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-to-unlock-the-potential-of-mobile-money.json"),
  get_dai_data("https://dai-global-developments.com/post-api/inexpensive-mobile-platform-connects-agribusinesses-to-work-together-better.json"),
  get_dai_data("https://dai-global-developments.com/post-api/linking-soldiers-civilians-across-west-central-africa-to-increase-stability-security.json"),
  get_dai_data("https://dai-global-developments.com/post-api/microinsurance-does-it-pay-off-for-the-poor.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mobile-services-for-the-unbanked-finding-a-viable-commercial-model.json"),
  get_dai_data("https://dai-global-developments.com/post-api/unleashing-cambodian-technical-knowledge.json"),
  get_dai_data("https://dai-global-developments.com/post-api/philippine-city-launches-mobile-payment-pilot.json"),
  get_dai_data("https://dai-global-developments.com/post-api/rwandan-national-park-project-honored-as-world-s-best-by-british-travel-writers.json"),
  get_dai_data("https://dai-global-developments.com/post-api/savings-groups-and-financial-inclusion.json"),
  get_dai_data("https://dai-global-developments.com/post-api/the-service-provider-spectrum-from-microfinance-to-financial-inclusion.json"),
  get_dai_data("https://dai-global-developments.com/post-api/using-hard-data-to-inform-hiv-aids-interventions-for-economic-strengthening.json"),
  get_dai_data("https://dai-global-developments.com/post-api/bottom-up-decentralization-new-local-autonomy-kickstarts-community-governing-in-the-drc.json"),
  get_dai_data("https://dai-global-developments.com/post-api/after-typhoon-haiyan-how-do-we-build-back-better.json"),
  get_dai_data("https://dai-global-developments.com/post-api/competitiveness-driven-growth-ciber-process-breaks-barriers-for-moldovan-entrepreneurs.json"),
  get_dai_data("https://dai-global-developments.com/post-api/ensuring-that-forest-communities-own-redd-projects-not-the-other-way-around.json"),
    get_dai_data("https://dai-global-developments.com/post-api/evidence-kits-turning-the-tide-on-sexual-violence.json"),
  get_dai_data("https://dai-global-developments.com/post-api/fiscal-project-helps-jordan-issue-1-25-billion-bond-saving-millions-for-development.json"),
  get_dai_data("https://dai-global-developments.com/post-api/foreseeing-a-grave-crisis-will-india-embrace-greater-water-use-efficiency.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-sub-saharan-africa-it-s-time-to-recognize-customary-land-rights.json"),
  get_dai_data("https://dai-global-developments.com/post-api/incentive-for-moroccan-farmers-to-conserve-water-increased-incomes.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mining-for-answers-mozambique-weighs-options-for-a-practical-profitable-local-content-policy.json"),
  get_dai_data("https://dai-global-developments.com/post-api/facilitating-e-banking-in-the-philippines.json"),
  get_dai_data("https://dai-global-developments.com/post-api/three-things-that-really-mattered-to-developing-the-youth-workforce-in-serbia-s-down-economy.json"),
  get_dai_data("https://dai-global-developments.com/post-api/to-unlock-job-growth-in-egypt-fix-the-micro-bee.json"),
  get_dai_data("https://dai-global-developments.com/post-api/dfid-project-assists-local-groups-in-sending-thousands-of-pakistani-boys-and-girls-to-school.json"),
  get_dai_data("https://dai-global-developments.com/post-api/natural-resource-conservation-through-electronic-hotel-reservations.json"),
  get_dai_data("https://dai-global-developments.com/post-api/the-partnership-fund.json"),
  get_dai_data("https://dai-global-developments.com/post-api/calculating-the-fiscal-cost-to-jordan-of-the-syrian-refugee-crisis.json"),
  get_dai_data("https://dai-global-developments.com/post-api/fertilizing-method-delivers-results-for-liberian-rice-farmers.json"),
  get_dai_data("https://dai-global-developments.com/post-api/going-social-on-avian-influenza.json"),
  get_dai_data("https://dai-global-developments.com/post-api/innovative-fund-enables-philippine-water-utilities-to-invest-deliver-safe-water-to-new-customers.json"),
  get_dai_data("https://dai-global-developments.com/post-api/poverty-partnership-and-the-pursuit-of-innovation.json"),
  get_dai_data("https://dai-global-developments.com/post-api/reforming-business-policy-in-mozambique-from-the-inside.json"),
  get_dai_data("https://dai-global-developments.com/post-api/dai-solutions-thinking-outside-the-organizational-box.json"),
  get_dai_data("https://dai-global-developments.com/post-api/afterword-with-rick-barton.json"),
  get_dai_data("https://dai-global-developments.com/post-api/building-economic-resilience-among-the-poor.json"),
    get_dai_data("https://dai-global-developments.com/post-api/zimbabwe-agriculture-project-finds-ways-to-engage-smallholder-farmers-despite-covid-19.json"),
  get_dai_data("https://dai-global-developments.com/post-api/this-time-it-s-different-a-new-measure-of-competitiveness-now-including-nature.json"),
  get_dai_data("https://dai-global-developments.com/post-api/steam-education-goes-online-with-launch-of-stemazone-platform-in-oman.json"),
  get_dai_data("https://dai-global-developments.com/post-api/health-equity-is-key-to-global-health-security-goals-learning-from-covid-19.json"),
  get_dai_data("https://dai-global-developments.com/post-api/world-bank-project-aims-to-rebuild-gaza-solar-facility-in-wake-of-conflict.json"),
  get_dai_data("https://dai-global-developments.com/post-api/usaid-projects-work-together-to-bolster-trade-between-pakistan-and-central-asia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/early-warning-and-response-system-increases-school-enrollment-and-retention.json"),
  get_dai_data("https://dai-global-developments.com/post-api/eu-forest-project-in-liberia-tackles-deforestation-and-paves-the-way-for-stability.json"),
  get_dai_data("https://dai-global-developments.com/post-api/power-grabbing-in-the-post-pandemic-era-demands-targeted-locally-driven-responses.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-innovative-storage-solutions-to-improve-energy-access-in-emerging-markets.json"),
  get_dai_data("https://dai-global-developments.com/post-api/usaid-s-partnership-approach-leaves-philippines-wildlife-in-safer-hands.json"),
  get_dai_data("https://dai-global-developments.com/post-api/natural-capital-exploring-a-financial-method-to-evaluate-its-cost.json"),
  get_dai_data("https://dai-global-developments.com/post-api/icai-highlights-awef-success-factors-relevant-to-employment-programming.json"),
  get_dai_data("https://dai-global-developments.com/post-api/malawi-s-land-governance-is-headed-in-the-right-direction.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-with-protect-wildlife-leader-rebecca-paz-biodiversity-conservation-and-local-development-can-go-hand-in-hand.json"),
  get_dai_data("https://dai-global-developments.com/post-api/cop26-is-a-chance-to-do-justice-to-people-and-planet.json"),
  get_dai_data("https://dai-global-developments.com/post-api/land-and-climate-lessons-from-ethiopia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/the-crucial-role-of-social-protection-systems-in-building-resilience-to-climate-risks.json"),
  get_dai_data("https://dai-global-developments.com/post-api/modernized-honduran-judicial-system-promises-lower-costs-increased-efficiency-safer-communities-and-greater-transparency.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mainstreaming-climate-smart-approaches-at-all-levels-of-ethiopian-society.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-switching-to-renewable-energy-is-an-urgent-priority-in-batloun-lebanon.json"),
  get_dai_data("https://dai-global-developments.com/post-api/climate-change-governance-six-lessons-learned.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-making-clean-energy-finance-work-in-vietnam.json"),
  get_dai_data("https://dai-global-developments.com/post-api/data-makes-a-difference-how-we-are-tackling-the-next-pandemic.json"),
  get_dai_data("https://dai-global-developments.com/post-api/facilitating-gender-smart-investing.json"),
  get_dai_data("https://dai-global-developments.com/post-api/gender-smart-investing-the-arab-women-s-enterprise-fund.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-how-the-one-health-approach-is-evolving-more-sustainably-and-inclusively.json"),
  get_dai_data("https://dai-global-developments.com/post-api/transforming-the-ukrainian-financial-sector.json"),
  get_dai_data("https://dai-global-developments.com/post-api/four-reasons-entrepreneurship-programs-should-invest-in-alumni-networks.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-to-design-nutrition-programs-to-increase-health-equity.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-municat-climate-adaptation-tool-fills-the-missing-middle.json"),
  get_dai_data("https://dai-global-developments.com/post-api/local-governance-chipping-away-at-corruption.json"),
  get_dai_data("https://dai-global-developments.com/post-api/three-key-elements-in-developing-local-content-policy-for-the-renewables-sector.json"),
  get_dai_data("https://dai-global-developments.com/post-api/a-strong-innovation-ecosystem-relies-on-financially-sustainable-incubators-and-accelerators.json"),
  get_dai_data("https://dai-global-developments.com/post-api/south-africa-s-green-energy-transformation-is-a-test-case-we-should-all-be-watching.json"),
  get_dai_data("https://dai-global-developments.com/post-api/four-ways-to-tackle-corruption-in-health-supply-chains.json"),
  get_dai_data("https://dai-global-developments.com/post-api/strengthening-south-africa-s-public-sector-capacity-to-drive-sustainable-development.json"),
  get_dai_data("https://dai-global-developments.com/post-api/health-equity-for-women-and-girls-requires-cultural-change-participation-and-local-influencers.json"),
  get_dai_data("https://dai-global-developments.com/post-api/ramping-up-gender-based-violence-prevention-risk-mitigation-and-response.json"),
  get_dai_data("https://dai-global-developments.com/post-api/beyond-the-washroom-sustainable-systemwide-approaches-for-good-sanitation.json"),
  get_dai_data("https://dai-global-developments.com/post-api/sounding-board-gives-youth-a-voice-in-development-decision-making.json"),
  get_dai_data("https://dai-global-developments.com/post-api/bouncing-back-success-factors-to-health-system-resilience.json"),
  get_dai_data("https://dai-global-developments.com/post-api/engaging-the-health-sector-in-gbv-prevention-and-response.json"),
  get_dai_data("https://dai-global-developments.com/post-api/green-bonds-and-good-governance-accelerate-investment-in-climate-smart-solutions-in-egypt.json"),
  get_dai_data("https://dai-global-developments.com/post-api/supporting-environmental-health-through-governance-reform.json"),
  get_dai_data("https://dai-global-developments.com/post-api/it-s-time-forensic-timber-tracing-became-mainstream.json"),
  get_dai_data("https://dai-global-developments.com/post-api/five-lessons-on-effectively-improving-the-water-sector.json"),
  get_dai_data("https://dai-global-developments.com/post-api/worker-health-and-wellbeing-programs-key-to-supply-chain-resilience.json"),
  get_dai_data("https://dai-global-developments.com/post-api/financing-sustainable-land-use-three-models-from-brazil.json"),
  get_dai_data("https://dai-global-developments.com/post-api/green-africa-development-justice-and-resilience.json"),
  get_dai_data("https://dai-global-developments.com/post-api/climate-and-health-what-it-means-to-have-the-unep-join-the-one-health-alliance.json"),
  get_dai_data("https://dai-global-developments.com/post-api/health-security-is-everyone-s-business.json"),
  get_dai_data("https://dai-global-developments.com/post-api/seed-trade-in-southern-africa-operationalizing-15-years-of-policy-in-six-years.json"),
  get_dai_data("https://dai-global-developments.com/post-api/hybrid-finance-model-shows-promise-in-boosting-access-to-sanitation.json"),
  get_dai_data("https://dai-global-developments.com/post-api/governments-are-crucial-to-locally-led-development.json"),
  get_dai_data("https://dai-global-developments.com/post-api/there-are-42-000-young-people-ready-to-lead-tanzania-s-economic-growth.json"),
  get_dai_data("https://dai-global-developments.com/post-api/making-a-difference-in-orangutan-conservation.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mainstreaming-gender-equity-and-inclusion-in-honduran-schools.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-countries-can-meet-their-family-planning-commitments.json"),
  get_dai_data("https://dai-global-developments.com/post-api/meeting-kenya-s-water-needs-by-positioning-utilities-for-success.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mexico-toward-a-gender-sensitive-energy-transition.json"),
  get_dai_data("https://dai-global-developments.com/post-api/u-s-offshore-wind-s-local-content-rules-provide-opportunity-for-investors.json"),
  get_dai_data("https://dai-global-developments.com/post-api/net-zero-update.json"),
  get_dai_data("https://dai-global-developments.com/post-api/funding-climate-action-in-the-south-mediterranean.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-ethiopia-can-develop-a-more-sustainable-health-supply-chain.json"),
  get_dai_data("https://dai-global-developments.com/post-api/regional-trade-bolsters-southern-africa-s-economic-outlook.json"),
  get_dai_data("https://dai-global-developments.com/post-api/communities-are-key-to-stopping-the-next-pandemic.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mobilizing-all-colombians-in-the-fight-against-corruption.json"),
  get_dai_data("https://dai-global-developments.com/post-api/breaking-barriers-to-learning-building-a-stronger-education-system-in-nigeria.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-how-climate-finance-is-critical-to-prevent-future-backsliding.json"),
  get_dai_data("https://dai-global-developments.com/post-api/synthesizing-the-sensitive-lessons-from-a-political-economy-analysis-in-a-closed-environment.json"),
  get_dai_data("https://dai-global-developments.com/post-api/one-year-on-how-one-usaid-governance-project-in-ukraine-pivoted-in-war-time.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mindthegap-a-development-finance-primer.json"),
  get_dai_data("https://dai-global-developments.com/post-api/local-and-national-public-and-private-resilient-education-systems-in-the-covid-19-era.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-high-impact-businesses-in-emerging-markets-are-pivoting-in-the-covid-19-crisis.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-donor-funded-economic-growth-projects-are-adapting-to-the-challenges-of-covid-19.json"),
  get_dai_data("https://dai-global-developments.com/post-api/stay-the-course-a-decade-of-focus-on-economic-reforms-pays-off-in-ukraine.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mobilizing-the-haitian-diaspora-to-invest-back-home.json"),
  get_dai_data("https://dai-global-developments.com/post-api/development-during-quarantine-lessons-from-four-usaid-projects.json"),
  get_dai_data("https://dai-global-developments.com/post-api/commercializing-agricultural-innovations-in-the-age-of-covid-19.json"),
  get_dai_data("https://dai-global-developments.com/post-api/gender-based-violence-on-the-rise-in-the-covid-19-era.json"),
  get_dai_data("https://dai-global-developments.com/post-api/a-shift-in-mindset-distance-learning-during-covid-19-boosts-participation-in-honduras.json"),
  get_dai_data("https://dai-global-developments.com/post-api/a-digital-tool-to-get-the-world-moving-again.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-with-jeffrey-mecaskey-how-community-engagement-regulations-and-incentives-build-a-path-to-improved-healthcare.json"),
  get_dai_data("https://dai-global-developments.com/post-api/empowering-women-lessons-from-covid-19-and-beyond.json"),
  get_dai_data("https://dai-global-developments.com/post-api/oman-s-journey-to-in-country-value-an-approach-to-local-content-that-works-for-government-and-the-private-sector.json"),
  get_dai_data("https://dai-global-developments.com/post-api/trade-in-the-time-of-covid-19-risk-or-opportunity.json"),
  get_dai_data("https://dai-global-developments.com/post-api/why-aligning-with-the-sdgs-helps-energy-companies-position-for-growth-and-how-to-do-it.json"),
  get_dai_data("https://dai-global-developments.com/post-api/fiscal-decentralization-builds-citizen-trust-positions-ukraine-for-european-future.json"),
  get_dai_data("https://dai-global-developments.com/post-api/strengthening-the-covid-19-response-and-protecting-health-services-in-uganda.json"),
  get_dai_data("https://dai-global-developments.com/post-api/market-system-lens-pays-dividends-for-northern-haiti-s-cacao-sector.json"),
  get_dai_data("https://dai-global-developments.com/post-api/dai-hosts-ande-west-africa-workshop-how-incubators-and-accelerators-can-build-corporate-partnerships.json"),
  get_dai_data("https://dai-global-developments.com/post-api/supporting-women-s-inclusion-through-community-development-in-pakistan.json"),
  get_dai_data("https://dai-global-developments.com/post-api/building-bridges-to-a-better-future-for-vulnerable-young-salvadorans.json"),
  get_dai_data("https://dai-global-developments.com/post-api/empowering-nurses-to-strengthen-the-mexican-health-system.json"),
  get_dai_data("https://dai-global-developments.com/post-api/opening-the-tap-a-coordinated-approach-to-facilitating-green-finance-for-smes-in-frontier-and-emerging-markets.json"),
  get_dai_data("https://dai-global-developments.com/post-api/good-news-dasgupta-just-raised-the-bar-for-your-company.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-with-donald-lunan-head-of-dai-s-new-climate-business-unit.json"),
  get_dai_data("https://dai-global-developments.com/post-api/2030-the-transition-to-a-low-carbon-economy-must-be-swift-and-fair.json"),
  get_dai_data("https://dai-global-developments.com/post-api/reaching-the-needs-of-all-citizens-in-a-more-democratic-pakistan.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-covid-19-is-highlighting-inequality-and-the-role-for-social-protection.json"),
  get_dai_data("https://dai-global-developments.com/post-api/what-we-have-learned-through-land-reform-implementation-in-malawi.json"),
  get_dai_data("https://dai-global-developments.com/post-api/now-more-than-ever-safeguarding-in-a-time-of-crisis.json"),
  get_dai_data("https://dai-global-developments.com/post-api/usaid-local-governance-activity-supports-health-systems-to-prevent-spread-of-covid-19-in-honduras.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-a-conversation-with-jenny-baker-dai-global-health-senior-vice-president.json"),
  get_dai_data("https://dai-global-developments.com/post-api/transitioning-a-supply-base-from-offshore-oil-and-gas-to-marine-renewables.json"),
  get_dai_data("https://dai-global-developments.com/post-api/avoiding-credit-risk-contagion-in-frontier-and-emerging-economies.json"),
  get_dai_data("https://dai-global-developments.com/post-api/curbing-irregular-migration-shifting-focus-from-the-american-dream-to-the-honduran-reality.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-can-we-support-the-private-sector-in-vulnerable-and-developing-economies-following-covid-19.json"),
  get_dai_data("https://dai-global-developments.com/post-api/here-s-how-we-push-ahead-with-inclusive-education.json"),
  get_dai_data("https://dai-global-developments.com/post-api/covid-19-public-financial-management-solutions-for-the-immediate-and-longer-term.json"),
  get_dai_data("https://dai-global-developments.com/post-api/usaid-supported-enterprise-in-ukraine-repairs-lung-ventilators-for-use-in-covid-19-crisis.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-europeaid-s-pakistan-brace-programme-is-engaging-communities-in-the-covid-19-era.json"),
  get_dai_data("https://dai-global-developments.com/post-api/it-s-getting-easier-to-do-business-in-nigeria-how-the-award-winning-policy-development-facility-supported-reform.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-ethiopia-keeping-land-rights-on-the-agenda-through-the-pandemic.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-a-place-based-approach-built-climate-resilience-in-indonesia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-knowledge-management-helps-make-remote-work-work.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-can-digital-financial-services-be-utilised-in-response-to-covid-19.json"),
  get_dai_data("https://dai-global-developments.com/post-api/improving-safety-net-programmes-to-include-those-most-vulnerable-to-climate-change.json"),
  get_dai_data("https://dai-global-developments.com/post-api/eu-investment-guarantees-begin-to-deliver-on-the-promise-of-development-finance.json"),
  get_dai_data("https://dai-global-developments.com/post-api/lift-ensuring-women-and-vulnerable-groups-reap-full-benefits-of-land-certification-in-ethiopia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/using-a-market-systems-approach-to-curb-human-trafficking-and-irregular-migration-in-nigeria.json"),
  get_dai_data("https://dai-global-developments.com/post-api/hot-enough-for-you-four-steps-to-help-the-world-keep-its-cool.json"),
  get_dai_data("https://dai-global-developments.com/post-api/nine-lessons-learned-the-not-so-simple-task-of-obtaining-land-rights.json"),
  get_dai_data("https://dai-global-developments.com/post-api/through-the-looking-glass-the-many-ways-to-invest-in-greater-gender-equity.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-dai-global-health-s-chris-legrand-on-the-launch-of-his-new-book.json"),
  get_dai_data("https://dai-global-developments.com/post-api/all-systems-go-usaid-s-private-sector-led-approach-pays-dividends-in-bangladesh.json"),
  get_dai_data("https://dai-global-developments.com/post-api/supporting-a-human-centered-home-health-system-in-jordan.json"),
  get_dai_data("https://dai-global-developments.com/post-api/can-the-development-community-adopt-agile.json"),
  get_dai_data("https://dai-global-developments.com/post-api/finding-meaning-in-the-j2sr-metrics.json"),
  get_dai_data("https://dai-global-developments.com/post-api/safe-learning-spaces-in-honduras-curb-undocumented-migration.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-john-leckie-on-what-s-next-for-dai-s-land-practice.json"),
  get_dai_data("https://dai-global-developments.com/post-api/investments-in-off-grid-energy-businesses-are-bringing-electricity-to-hundreds-of-thousands-in-kenya.json"),
  get_dai_data("https://dai-global-developments.com/post-api/paving-the-way-for-green-energy-financing-in-the-mediterranean.json"),
  get_dai_data("https://dai-global-developments.com/post-api/investing-in-the-underdogs-boosting-local-leadership-in-burma.json"),
  get_dai_data("https://dai-global-developments.com/post-api/to-go-where-we-re-going-we-need-to-meet-investors-where-they-live.json"),
  get_dai_data("https://dai-global-developments.com/post-api/adopting-a-private-sector-led-approach-to-advance-digital-startups-in-cambodia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/new-research-offers-alternatives-for-frontier-market-venture-capital-and-private-equity.json"),
  get_dai_data("https://dai-global-developments.com/post-api/social-protection-in-somalia-can-bridge-short-and-long-term-solutions.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-ehat-miftaraj-anti-corruption-expert-on-the-prospect-for-rule-of-law-reform-in-kosovo.json"),
  get_dai_data("https://dai-global-developments.com/post-api/blended-finance-case-study-gaza-industrial-estate-solar-energy-rooftop.json"),
  get_dai_data("https://dai-global-developments.com/post-api/blended-finance-tools-offer-a-new-approach-to-an-old-problem.json"),
  get_dai_data("https://dai-global-developments.com/post-api/it-s-not-too-late-to-prepare-for-covid-19.json"),
  get_dai_data("https://dai-global-developments.com/post-api/extending-education-access-to-vulnerable-young-salvadorans.json"),
  get_dai_data("https://dai-global-developments.com/post-api/restoring-trust-toward-a-people-centric-security-sector-in-the-gambia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/the-complexity-of-building-a-market-for-certified-seeds-a-case-study-from-mozambique.json"),
  get_dai_data("https://dai-global-developments.com/post-api/strengthening-women-s-control-over-land-inheritance-reform-in-tunisia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-guatemala-new-research-on-gender-equality-shapes-government-and-usaid-investments-in-taxation.json"),
  get_dai_data("https://dai-global-developments.com/post-api/transforming-social-protection-taking-a-gender-lens-to-nepal-s-social-security-allowance.json"),
  get_dai_data("https://dai-global-developments.com/post-api/covid-19-demands-new-thinking-on-local-content-in-oil-gas-and-mining.json"),
  get_dai_data("https://dai-global-developments.com/post-api/ethiopia-case-study-can-the-land-titling-process-mitigate-land-related-violence-against-women-and-vulnerable-groups.json"),
  get_dai_data("https://dai-global-developments.com/post-api/covid-19-this-pandemic-offers-a-lesson-we-must-learn-before-the-next.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-statistics-can-transform-governance-a-q-and-a-with-economist-and-statistician-jean-paul-zoyem.json"),
  get_dai_data("https://dai-global-developments.com/post-api/covid-19-low-cost-solutions-to-maintain-engagement-with-local-partners-in-the-supply-chain.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-somalia-ensuring-social-protection-during-the-covid-19-pandemic-and-food-security-crisis.json"),
  get_dai_data("https://dai-global-developments.com/post-api/sourcing-the-wadi-how-palestinian-workers-are-filling-niche-needs-in-israel-s-it-sector.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-with-dai-s-susan-scribner-preparedness-response-and-global-health-security.json"),
  get_dai_data("https://dai-global-developments.com/post-api/eu-funds-totaling-4-1-billion-aim-to-boost-investment-private-sector-engagement-in-africa-and-european-neighbourhood-countries.json"),
  get_dai_data("https://dai-global-developments.com/post-api/new-orangutan-species-discovered-in-forest-supported-by-usaid-conservation-program.json"),
  get_dai_data("https://dai-global-developments.com/post-api/to-realize-the-promise-of-renewables-address-the-concerns-of-local-people.json"),
  get_dai_data("https://dai-global-developments.com/post-api/gathering-the-evidence-to-mobilize-domestic-resources-for-health-care.json"),
  get_dai_data("https://dai-global-developments.com/post-api/women-s-land-rights-and-the-problem-of-polygamy-a-proposal-in-ethiopia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/liberia-moves-to-reduce-donor-dependence-by-improving-its-ability-to-invest-in-itself.json"),
  get_dai_data("https://dai-global-developments.com/post-api/with-elections-looming-can-pakistan-fulfill-its-education-promise-to-unschooled-children.json"),
  get_dai_data("https://dai-global-developments.com/post-api/philippines-new-tax-bill-promises-more-revenue-for-social-programs-infrastructure.json"),
  get_dai_data("https://dai-global-developments.com/post-api/new-zealand-aid-helps-rwandan-smallholders-enter-fortified-foods-supply-chain.json"),
  get_dai_data("https://dai-global-developments.com/post-api/ec-helps-position-the-southern-africa-development-community-for-21st-century-success.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-nigeria-governance-champions-can-transform-resource-wealth-into-development-results.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mozambique-even-a-progressive-land-law-needs-revision-after-a-generation-of-experience.json"),
  get_dai_data("https://dai-global-developments.com/post-api/lta-program-shows-benefit-of-truly-participatory-approach.json"),
  get_dai_data("https://dai-global-developments.com/post-api/36-million-investment-partnership-finances-warehouses-in-malawi-to-improve-food-security.json"),
  get_dai_data("https://dai-global-developments.com/post-api/young-rural-women-are-crucial-to-advancing-universal-health-coverage-in-northern-nigeria.json"),
  get_dai_data("https://dai-global-developments.com/post-api/ethiopia-stands-poised-to-lead-an-african-industrial-revolution.json"),
  get_dai_data("https://dai-global-developments.com/post-api/blended-finance-in-action-how-usaid-leveraged-100-million-in-east-africa.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-can-nigeria-fulfill-its-broad-economic-potential.json"),
  get_dai_data("https://dai-global-developments.com/post-api/new-dfid-guidance-aims-to-improve-emergency-schooling-for-millions-of-displaced-children.json"),
  get_dai_data("https://dai-global-developments.com/post-api/with-u-k-aid-lebanon-s-social-enterprises-pilot-a-new-model-of-development.json"),
  get_dai_data("https://dai-global-developments.com/post-api/can-we-keep-the-promise-mobilizing-business-on-the-refugee-frontline-in-jordan.json"),
  get_dai_data("https://dai-global-developments.com/post-api/addressing-jordan-s-youth-unemployment-bubble-usaid-program-aligns-workforce-with-emerging-opportunities.json"),
  get_dai_data("https://dai-global-developments.com/post-api/new-generation-of-ec-framework-contracts-offers-agile-programming-for-european-development-aid.json"),
  get_dai_data("https://dai-global-developments.com/post-api/four-recommendations-for-strengthening-seed-systems.json"),
  get_dai_data("https://dai-global-developments.com/post-api/global-health-and-tech-thinkers-come-together-at-switchpoint.json"),
  get_dai_data("https://dai-global-developments.com/post-api/africa-trading-five-takeaways-on-trade-based-solutions-for-food-security.json"),
  get_dai_data("https://dai-global-developments.com/post-api/liberia-launches-mobile-tax-payments-opening-doors-to-increased-revenue-for-domestic-development.json"),
  get_dai_data("https://dai-global-developments.com/post-api/dfid-programme-helps-establish-business-equipment-leasing-in-sub-saharan-africa-s-largest-country.json"),
  get_dai_data("https://dai-global-developments.com/post-api/zambia-pilot-demonstrates-how-to-save-lives-scale-relief-for-children-suffering-from-malaria.json"),
  get_dai_data("https://dai-global-developments.com/post-api/agriculture-finance-with-a-climate-lens-takes-off-in-kenya.json"),
  get_dai_data("https://dai-global-developments.com/post-api/collaboration-is-essential-to-improving-maternal-and-newborn-health-in-indonesia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/health-system-in-haiti-takes-key-step-by-launching-national-tuberculosis-tracker.json"),
  get_dai_data("https://dai-global-developments.com/post-api/using-market-driven-strategies-to-reduce-poverty-and-human-trafficking-in-nigeria.json"),
  get_dai_data("https://dai-global-developments.com/post-api/placing-women-at-the-center-of-water-supply-management-in-kenya.json"),
  get_dai_data("https://dai-global-developments.com/post-api/keep-up-the-fight-for-high-quality-education-for-all-in-pakistan.json"),
  get_dai_data("https://dai-global-developments.com/post-api/jordan-embraces-renewables-to-fuel-its-economy.json"),
  get_dai_data("https://dai-global-developments.com/post-api/demand-for-private-capital-draws-usaid-units-to-invest-program.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-can-developing-countries-identify-and-allocate-resources-to-pay-for-health-services.json"),
  get_dai_data("https://dai-global-developments.com/post-api/baseline-study-prompts-school-officials-to-counter-violence-in-honduras.json"),
  get_dai_data("https://dai-global-developments.com/post-api/land-titles-in-ethiopia-open-doors-to-finance-and-investment.json"),
  get_dai_data("https://dai-global-developments.com/post-api/beyond-boundaries-how-secure-land-tenure-is-improving-lives-in-rural-tanzania.json"),
  get_dai_data("https://dai-global-developments.com/post-api/case-study-a-market-systems-approach-to-deriving-value-from-land-certificates-in-ethiopia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/case-study-overcoming-land-tenure-issues-to-stimulate-investment-in-mozambique.json"),
  get_dai_data("https://dai-global-developments.com/post-api/putting-the-value-in-land-titling.json"),
  get_dai_data("https://dai-global-developments.com/post-api/can-online-dispute-resolution-change-the-way-global-msmes-do-business.json"),
  get_dai_data("https://dai-global-developments.com/post-api/four-steps-to-advocate-for-government-investment-in-public-health.json"),
  get_dai_data("https://dai-global-developments.com/post-api/why-the-time-is-right-for-access-for-all.json"),
  get_dai_data("https://dai-global-developments.com/post-api/building-inclusivity-into-inclusive-education.json"),
  get_dai_data("https://dai-global-developments.com/post-api/will-feminized-parliaments-mean-more-gender-friendly-policies.json"),
  get_dai_data("https://dai-global-developments.com/post-api/improving-livestock-markets-to-generate-economic-growth-and-resilience-in-east-africa.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-uganda-local-hearings-show-accountability-in-action.json"),
  get_dai_data("https://dai-global-developments.com/post-api/invest-on-the-frontier-of-gender-lens-investing.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-to-ensure-voluntary-sustainability-standards-are-more-effective-in-promoting-gender-equality-in-global-value-chains.json"),
  get_dai_data("https://dai-global-developments.com/post-api/now-more-competitive-jordan-s-pharmaceuticals-see-healthy-jump-in-exports.json"),
  get_dai_data("https://dai-global-developments.com/post-api/getting-creative-with-transportation-for-el-salvador-s-young-job-seekers.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-el-salvador-outsourcing-remote-programming-jobs-to-youth-outside-the-capital.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-el-salvador-shifting-employer-perceptions-while-getting-youth-work-ready.json"),
  get_dai_data("https://dai-global-developments.com/post-api/three-ways-to-make-hiring-more-inclusive-of-vulnerable-youth-lessons-from-el-salvador.json"),
  get_dai_data("https://dai-global-developments.com/post-api/dai-global-health-partner-thinkmd-embarks-on-new-projects-in-kenya-and-indonesia-with-save-the-children.json"),
  get_dai_data("https://dai-global-developments.com/post-api/hold-the-charcoal-diverting-sub-saharan-africa-s-demand-for-a-destructive-energy-source.json"),
  get_dai_data("https://dai-global-developments.com/post-api/partnering-for-social-good-what-s-in-it-for-all-of-us.json"),
  get_dai_data("https://dai-global-developments.com/post-api/building-a-bridge-to-the-new-era-of-usaid-assistance.json"),
  get_dai_data("https://dai-global-developments.com/post-api/lebanon-s-cornucopia-value-chain-project-unleashes-potential-of-10-sectors.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mark-your-calendar-it-s-may-21.json"),
  get_dai_data("https://dai-global-developments.com/post-api/hard-fought-wins-reaffirm-the-value-of-working-with-palestine-s-private-sector.json"),
  get_dai_data("https://dai-global-developments.com/post-api/in-guatemala-assisting-municipalities-to-improve-governance-services-and-self-reliance.json"),
  get_dai_data("https://dai-global-developments.com/post-api/savings-groups-enabling-hundreds-of-smallholders-in-mozambique-to-buy-certified-seed.json"),
  get_dai_data("https://dai-global-developments.com/post-api/engaging-both-men-and-women-to-link-nutrition-to-agriculture.json"),
  get_dai_data("https://dai-global-developments.com/post-api/scaling-up-mobile-health-services-to-expectant-and-new-mothers-in-cambodia.json"),
  get_dai_data("https://dai-global-developments.com/post-api/positively-mobilizing-urban-communities-for-wash.json"),
  get_dai_data("https://dai-global-developments.com/post-api/energizing-the-support-network-for-people-with-disabilities-in-vietnam.json"),
  get_dai_data("https://dai-global-developments.com/post-api/when-tax-reform-leads-to-increased-funding-for-health-services.json"),
  get_dai_data("https://dai-global-developments.com/post-api/a-good-use-of-u-s-taxpayer-money-helping-countries-mobilize-domestic-resources.json"),
  get_dai_data("https://dai-global-developments.com/post-api/servir-demand-activity-a-key-link-in-connecting-space-to-village.json"),
  get_dai_data("https://dai-global-developments.com/post-api/clean-water-for-all-by-2030-no-really.json"),
  get_dai_data("https://dai-global-developments.com/post-api/usaid-backed-fellow-inspires-malaysian-renewable-energy-policy.json"),
  get_dai_data("https://dai-global-developments.com/post-api/zika-and-the-americas-a-call-to-action-for-surveillance-and-preparedness.json"),
  get_dai_data("https://dai-global-developments.com/post-api/plugging-in-to-jordan-s-rising-demand-for-electric-cars.json"),
  get_dai_data("https://dai-global-developments.com/post-api/unlocking-local-content-harnessing-the-power-of-data-driven-decision-making.json"),
  get_dai_data("https://dai-global-developments.com/post-api/big-data-and-domestic-resource-mobilization-how-donors-can-help-developing-countries-increase-revenue.json"),
  get_dai_data("https://dai-global-developments.com/post-api/domestic-resource-mobilization-takes-root-in-el-salvador-and-beyond.json"),
  get_dai_data("https://dai-global-developments.com/post-api/agriculture-goes-prime-time-enthralling-a-tv-audience-of-future-farmers.json"),
  get_dai_data("https://dai-global-developments.com/post-api/new-opportunities-emerge-to-support-meaningful-democratic-reform-in-sri-lanka.json"),
  get_dai_data("https://dai-global-developments.com/post-api/unveiling-a-new-methodology-for-measuring-market-systems-and-their-impact-on-local-development.json"),
  get_dai_data("https://dai-global-developments.com/post-api/chevron-s-nigerian-initiative-found-to-decrease-business-risk-attract-local-investment-and-bring-hope.json"),
  get_dai_data("https://dai-global-developments.com/post-api/national-governments-hold-the-key-to-sustainable-local-climate-change-adaptation-in-the-mekong-basin.json"),
  get_dai_data("https://dai-global-developments.com/post-api/applying-market-systems-approaches-to-financial-inclusion-projects.json"),
  get_dai_data("https://dai-global-developments.com/post-api/learning-from-local-content-policies-insights-from-a-study-of-six-resource-rich-countries.json"),
  get_dai_data("https://dai-global-developments.com/post-api/mining-companies-and-startup-partners-should-begin-developing-local-content-before-breaking-ground.json"),
  get_dai_data("https://dai-global-developments.com/post-api/establishing-a-model-at-the-local-level-for-science-driven-climate-adaptation.json"),
  get_dai_data("https://dai-global-developments.com/post-api/market-systems-development-boosts-farming-nutrition-in-bangladesh-s-southern-delta.json"),
  get_dai_data("https://dai-global-developments.com/post-api/onshore-fish-farms-flourish-in-gaza.json"),
  get_dai_data("https://dai-global-developments.com/post-api/six-ways-to-mitigate-instability-in-central-america.json"),
  get_dai_data("https://dai-global-developments.com/post-api/delivering-large-scale-land-certification-programmes-lessons-from-rwanda.json"),
  get_dai_data("https://dai-global-developments.com/post-api/investing-leasing-land-and-compensating-landowners-the-addax-bioenergy-experience-in-sierra-leone.json"),
  get_dai_data("https://dai-global-developments.com/post-api/enhancing-women-and-girls-land-rights-in-rural-sierra-leone.json"),
  get_dai_data("https://dai-global-developments.com/post-api/legitimate-land-tenure-and-property-rights-fostering-compliance-and-development-outcomes.json"),
  get_dai_data("https://dai-global-developments.com/post-api/the-law-of-the-land-recent-cases-show-legal-support-for-local-people.json"),
  get_dai_data("https://dai-global-developments.com/post-api/a-call-to-arms-shaping-a-more-innovative-approach-to-adaptive-programming-in-democracy-assistance.json"),
  get_dai_data("https://dai-global-developments.com/post-api/ethiopia-land-registration-ready-for-lift-off-now-what.json"),
  get_dai_data("https://dai-global-developments.com/post-api/big-gains-in-access-to-safe-drinking-water-how-four-african-countries-did-it-and-how-others-can-too.json"),
  get_dai_data("https://dai-global-developments.com/post-api/unlocking-capital-how-usaid-pushed-the-frontier-of-financial-services-and-built-a-foundation-for-economic-growth-in-kenya.json"),
  get_dai_data("https://dai-global-developments.com/post-api/despite-regional-instability-lebanon-s-honey-sector-reaches-new-heights.json"),
  get_dai_data("https://dai-global-developments.com/post-api/public-private-partnerships-for-land-administration-can-it-work-in-cabo-verde.json"),
  get_dai_data("https://dai-global-developments.com/post-api/how-tax-and-budget-assistance-helps-developing-countries-help-themselves.json"),
  get_dai_data("https://dai-global-developments.com/post-api/the-whole-spectrum-a-holistic-approach-to-climate-resilience.json"),
  get_dai_data("https://dai-global-developments.com/post-api/dialogue-and-development-in-ghana-s-oil-and-gas-region.json"),
  get_dai_data("https://dai-global-developments.com/post-api/from-land-tenure-regularisation-to-a-sustainable-land-register.json"),
  get_dai_data("https://dai-global-developments.com/post-api/93-million-grain-deal-between-east-african-countries-demonstrates-how-the-region-can-feed-itself.json"),
  get_dai_data("https://dai-global-developments.com/post-api/making-land-rights-real.json"),
  get_dai_data("https://dai-global-developments.com/post-api/using-mobile-technology-for-first-registration-of-land-lessons-learned-in-tanzania.json"),
  get_dai_data("https://dai-global-developments.com/post-api/philippines-increases-tax-collections-by-1-1-billion-year-over-year-without-raising-rates.json"),
  get_dai_data("https://dai-global-developments.com/post-api/polseff-s-legacy-lower-energy-bills-for-businesses-across-poland-a-financing-model-to-scale-and-replicate.json"),
  get_dai_data("https://dai-global-developments.com/post-api/using-development-assistance-to-catalyze-sound-investments-in-emerging-and-developing-markets.json"),
  get_dai_data("https://dai-global-developments.com/post-api/cold-storage-expansion-drives-market-development-in-uzbekistan.json"),
  get_dai_data("https://dai-global-developments.com/post-api/new-possibilities-the-role-of-governance-in-countering-violent-extremism-in-iraq.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-barry-finette-on-the-hopes-and-challenges-for-thinkmd-s-life-saving-mhealth-platform.json"),
  get_dai_data("https://dai-global-developments.com/post-api/more-than-developing-apps-usaid-program-propels-cambodian-girls-into-global-technology-finals.json"),
  get_dai_data("https://dai-global-developments.com/post-api/q-and-a-unlocking-inclusive-economic-growth-for-mozambicans-by-building-a-market-for-digital-financial-inclusion.json"),
  get_dai_data("https://dai-global-developments.com/post-api/messe-frankfurt-s-purchase-of-source-africa-trade-show-exemplifies-the-potential-of-market-systems-development.json"),
  get_dai_data("https://dai-global-developments.com/post-api/helping-eastern-partnership-countries-meet-their-commitments-to-address-climate-change.json"),
  
]

# Chunk sources and build the search index
source_chunks = []
splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=0)
for source in sources:
    for chunk in splitter.split_text(source.page_content):
        source_chunks.append(Document(page_content=chunk, metadata=source.metadata))

search_index = FAISS.from_documents(source_chunks, OpenAIEmbeddings())

# Engineer prompt
template = """Generate a blog post with the title '{question}'. The post should be at least 2000 words long. {summaries}"""
PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])
chain = load_qa_with_sources_chain(OpenAI(model_name="text-davinci-003", max_tokens=1200, temperature=0.9), chain_type="stuff", prompt=PROMPT)

# Generate text
def gen_answer(question):
  print(
    chain(
      {
        "input_documents": search_index.similarity_search(question, k=4),
        "question": question,
      },
      return_only_outputs=True,
    )["output_text"]
  )

# Setup Slack Integration
import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
from threading import Thread
from queue import Queue, Full

SLACK_CHANNEL="#d-ai"
SLACK_TOKEN="xoxb-2190897728-5030141376935-fFwIcIn08qafOSzrzwHSmyHb"
SIGNING_SECRET="602db57a4a626be7b5a7d8e77ffe69be"

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

client = slack.WebClient(token=SLACK_TOKEN)

messages_to_handle = Queue(maxsize=32)

# Functions for intereacting with requests from Slack
# Replying back to Slack
def reply_to_slack(thread_ts, response):
    client.chat_postMessage(channel=SLACK_CHANNEL, text=response, thread_ts=thread_ts)
# Responding with a thumbs up to confirm message received
def confirm_message_received(channel, thread_ts):
    client.reactions_add(
        channel=channel,
        name="thumbsup",
        timestamp=thread_ts
    )
# A seperate thread for asking the AI for a response
def handle_message():
    while True:
        message_id, thread_ts, user_id, text = messages_to_handle.get()
        print(f'Handling message {message_id} with text {text}')
        text = " ".join(text.split(" ", 1)[1:])
        try:
            response = gen_answer(text)
            reply_to_slack(thread_ts, response)
        except Exception as e:
            response = f":exclamation::exclamation::exclamation: Error: {e}"
            reply_to_slack(thread_ts, response)
        finally:
            messages_to_handle.task_done()

@slack_event_adapter.on('app_mention')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    message_id = event.get('client_msg_id')
    thread_ts = event.get('ts')
    channel = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    try:
        messages_to_handle.put_nowait((message_id, thread_ts, user_id, text))
        confirm_message_received(channel, thread_ts)
    except Full:
        response = f":exclamation::exclamation::exclamation:Error: Too many requests"
        reply_to_slack(thread_ts, response)
    except Exception as e:
        response = f":exclamation::exclamation::exclamation: Error: {e}"
        reply_to_slack(thread_ts, response)
        print(e)

# @ slack_event_adapter.on('message')
# def message(payload):
#     print(payload)
#     event = payload.get('event', {})
#     channel_id = event.get('channel')

#     user_id = event.get('user')
#     text = event.get('text')
#     if text == "hi":
#         client.chat_postMessage(channel=channel_id,text="Oh, Hello There")

if __name__ == "__main__":
    Thread(target=handle_message, daemon=True).start()
    app.run(debug=True, port=8080)