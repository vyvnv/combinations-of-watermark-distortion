#ifndef E_BLIND_DLC
#define E_BLIND_DLC

#include "Watermark.h"
#include "Detector.h"

class EBlindDLC : public Watermark
{
public:
	EBlindDLC(double alpha = -1, double detectThreshold = -1, const std::vector<double> reference = std::vector<double>(), Detector::Type detectorType = Detector::LINEAR);
	virtual ~EBlindDLC();
	void setAlpha(double alpha);
	void setDetectThreshold(double detectThreshold);
	void setReference(std::vector<double>& reference);

	bool embed(std::shared_ptr<VideoFrame> pframe, bool value);
	DetectResult detect(const std::shared_ptr<VideoFrame> pframe);
	bool getCorrelation(const std::shared_ptr<VideoFrame> pframe, double& correlation);

//	static std::shared_ptr<VideoFrame> createReference(const std::shared_ptr<VideoFrame> pframe, int maxValue);
	static std::vector<double> createReference(const std::shared_ptr<VideoFrame> pframe);
	static void referenceStore(const std::vector<double>& data, const std::string& filename);
	static std::vector<double> referenceLoad(const std::string& filename);

private:
	DetectResult detectInternal(const std::shared_ptr<VideoFrame> pframe, double *pcorrelation);

	double                       m_alpha;
	double                       m_detectThreshold;
	std::vector<double>          m_reference;
	Detector::Type               m_detectorType;

};

#endif
